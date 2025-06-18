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
