from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import HealthRecord
from .health_recommend_model import get_health_recommendation_by_values
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg
from datetime import datetime, timedelta

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_health_record_and_recommend(request):
    """건강 기록 저장 및 AI 추천 API"""
    try:
        # 요청 데이터 받기
        systolic = request.data.get('systolic')
        diastolic = request.data.get('diastolic')
        glucose = request.data.get('glucose')
        notes = request.data.get('notes', '')
        
        # 필수 데이터 검증
        if not all([systolic, diastolic, glucose]):
            return Response({
                'error': '혈압(수축기, 이완기)과 혈당 수치가 모두 필요합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 숫자 변환 검증
        try:
            systolic = int(systolic)
            diastolic = int(diastolic)
            glucose = int(glucose)
        except ValueError:
            return Response({
                'error': '혈압과 혈당은 숫자로 입력해주세요.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # HealthRecord 저장
        health_record = HealthRecord.objects.create(
            user=request.user,
            record_date=timezone.now(),
            blood_pressure=f"{systolic}/{diastolic}",
            blood_sugar=glucose,
            notes=notes,
            health_condition="정상"
        )
        
        # AI 모델로 추천 생성
        recommendation = get_health_recommendation_by_values(systolic, diastolic, glucose)
        
        if 'error' in recommendation:
            return Response({
                'error': recommendation['error']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': True,
            'message': '건강 기록이 저장되고 추천이 생성되었습니다.',
            'data': {
                'health_record_id': health_record.id,
                'record_date': health_record.record_date.strftime('%Y-%m-%d %H:%M'),
                'blood_pressure': f"{systolic}/{diastolic}",
                'blood_sugar': glucose,
                'recommendation': recommendation
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'서버 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_health_records(request):
    """사용자의 건강 기록 목록 조회"""
    try:
        records = HealthRecord.objects.filter(user=request.user).order_by('-record_date')[:10]
        
        data = []
        for record in records:
            data.append({
                'id': record.id,
                'record_date': record.record_date.strftime('%Y-%m-%d %H:%M'),
                'blood_pressure': record.blood_pressure,
                'blood_sugar': record.blood_sugar,
                'notes': record.notes
            })
        
        return Response({
            'success': True,
            'data': data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'서버 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def health_recommendation_options(request):
    """사용 가능한 혈압/혈당 레벨 옵션을 반환하는 API"""
    return Response({
        'bp_levels': ['저혈압', '정상', '주의혈압', '고혈압전단계', '고혈압'],
        'glucose_levels': ['위험저혈당', '저혈당', '정상', '고혈당전단계', '당뇨진단기준', '심한고혈당'],
        'description': {
            'bp_levels': {
                '저혈압': '수축기 혈압 90mmHg 미만',
                '정상': '수축기 혈압 90-120mmHg',
                '주의혈압': '수축기 혈압 120-130mmHg',
                '고혈압전단계': '수축기 혈압 130-140mmHg',
                '고혈압': '수축기 혈압 140mmHg 이상'
            },
            'glucose_levels': {
                '위험저혈당': '공복 혈당 54mg/dL 미만',
                '저혈당': '공복 혈당 54-70mg/dL',
                '정상': '공복 혈당 70-100mg/dL',
                '고혈당전단계': '공복 혈당 100-126mg/dL',
                '당뇨진단기준': '공복 혈당 126-180mg/dL',
                '심한고혈당': '공복 혈당 180mg/dL 이상'
            }
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_health_summary(request):
    """최근 1주일간의 건강 데이터 평균치를 반환"""
    user = request.user
    week_ago = datetime.now().date() - timedelta(days=7)
    
    # 최근 1주일간의 건강 기록 조회
    recent_records = HealthRecord.objects.filter(
        user=user,
        record_date__date__gte=week_ago
    )
    
    if recent_records.exists():
        # 혈압과 혈당 데이터 수집
        blood_pressures = []
        blood_sugars = []
        
        for record in recent_records:
            # 혈압 데이터 파싱 (예: "120/80" 형태)
            if record.blood_pressure and '/' in record.blood_pressure:
                try:
                    systolic, diastolic = map(int, record.blood_pressure.split('/'))
                    blood_pressures.append((systolic, diastolic))
                except ValueError:
                    pass
            
            # 혈당 데이터
            if record.blood_sugar:
                blood_sugars.append(record.blood_sugar)
        
        # 평균 계산
        avg_blood_pressure = None
        if blood_pressures:
            avg_systolic = sum(bp[0] for bp in blood_pressures) / len(blood_pressures)
            avg_diastolic = sum(bp[1] for bp in blood_pressures) / len(blood_pressures)
            avg_blood_pressure = f"{round(avg_systolic)}/{round(avg_diastolic)}"
        
        avg_blood_sugar = None
        if blood_sugars:
            avg_blood_sugar = round(sum(blood_sugars) / len(blood_sugars))
        
        return Response({
            'avgBloodPressure': avg_blood_pressure,
            'avgBloodSugar': avg_blood_sugar,
            'recordCount': recent_records.count()
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'avgBloodPressure': None,
            'avgBloodSugar': None,
            'recordCount': 0
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation(request, date):
    """특정 날짜의 추천 정보를 반환"""
    user = request.user
    
    try:
        # 해당 날짜의 건강 기록 조회
        health_record = HealthRecord.objects.filter(
            user=user,
            record_date__date=date
        ).first()
        
        if health_record:
            # 임시로 더미 추천 데이터 반환 (실제로는 recommendation 필드가 있어야 함)
            return Response({
                '추천_운동': '가벼운 산책 30분, 스트레칭 10분',
                '추천_식단': '저염식, 채소 위주의 식단, 충분한 수분 섭취'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': '해당 날짜의 추천 정보가 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
