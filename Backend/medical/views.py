from django.http import JsonResponse
from .models import MedicalFacility
from .pill_algo import extract_pill_info
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Pill
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
def hospital_list(request):
    hospitals = MedicalFacility.objects.all()
    data = [{
        'id': hospital.id,
        'name': hospital.name,
        'address': hospital.address,
        'tel': hospital.tel,
        'type': hospital.type,
        'latitude': hospital.latitude,
        'longitude': hospital.longitude
    } for hospital in hospitals]
    return JsonResponse(data, safe=False)


# 약 업로드 API (기존 함수 이름 변경)
@csrf_exempt
def pill_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'error': '이미지가 없습니다'}, status=400)

        # 저장 경로를 MEDIA_ROOT 기준으로 설정
        save_path = os.path.join(settings.MEDIA_ROOT, image.name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        with open(save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # OCR 분석
        info = extract_pill_info(save_path)

        # DB 저장
        pill = Pill.objects.create(
            name=info['name'],
            type=info['type'],
            image=image,
            user=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({
            'message': '저장 완료',
            'pill_id': pill.id,
            'name': pill.name,
            'type': pill.get_type_display()
        })

    return JsonResponse({'error': 'POST 요청만 가능'}, status=405)


# 약 정보 넣는 부분
import os
from django.conf import settings

@csrf_exempt
def upload_pill_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({'error': '이미지가 없습니다'}, status=400)

        # 👇 저장 경로를 MEDIA_ROOT 기준으로 설정
        save_path = os.path.join(settings.MEDIA_ROOT, image.name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        with open(save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # OCR 분석
        info = extract_pill_info(save_path)

        # DB 저장
        pill = Pill.objects.create(
            name=info['name'],
            type=info['type'],
            image=image,  # 이건 원본 업로드 파일
            user=request.user if request.user.is_authenticated else None
        )

        return JsonResponse({
            'message': '저장 완료',
            'pill_id': pill.id,
            'name': pill.name,
            'type': pill.get_type_display()
        })

    return JsonResponse({'error': 'POST 요청만 가능'}, status=405)


@login_required
def pill_list(request):
    pills = Pill.objects.filter(user=request.user).order_by('-date_added')
    data = [
        {
            'id': pill.id,
            'name': pill.name,
            'type': pill.get_type_display(),
            'image': pill.image.url if pill.image else None,
            'date_added': pill.date_added.strftime('%Y-%m-%d %H:%M'),
        }
        for pill in pills
    ]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_pills(request):
    """사용자가 등록한 약 정보를 반환"""
    user = request.user
    
    # 사용자가 등록한 약 정보 조회
    pills = Pill.objects.filter(user=user).order_by('-date_added')
    
    pill_data = []
    for pill in pills:
        pill_data.append({
            'id': pill.id,
            'name': pill.name if pill.name else '약품명 미확인',
            'type': pill.get_type_display() if pill.type else '종류 미확인',
            'created_at': pill.date_added
        })
    
    return Response(pill_data, status=status.HTTP_200_OK)