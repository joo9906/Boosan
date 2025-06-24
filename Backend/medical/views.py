from django.http import JsonResponse
from .models import MedicalFacility, Pill
from .pill_algo import extract_pill_info
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import tempfile
import logging
import random
import uuid

logger = logging.getLogger(__name__)

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

@csrf_exempt
def upload_pill_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            if not image:
                return JsonResponse({'error': '이미지가 없습니다'}, status=400)

            # 이미지 파일 확장자 검사
            allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
            file_ext = os.path.splitext(image.name)[1].lower()
            if file_ext not in allowed_extensions:
                return JsonResponse({'error': '지원하지 않는 이미지 형식입니다'}, status=400)

            # Windows 환경에 맞는 임시 파일 경로 사용
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, image.name)
            
            try:
                with open(temp_path, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

                info = extract_pill_info(temp_path)
                if not info['name'] or info['name'] == '알 수 없는 약':
                    return JsonResponse({'error': '약 정보를 인식할 수 없습니다'}, status=400)

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
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                return JsonResponse({'error': '이미지 처리 중 오류가 발생했습니다'}, status=500)
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception as e:
                        logger.error(f"Error deleting temporary file: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': '서버 오류가 발생했습니다'}, status=500)

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

@csrf_exempt
def create_quiz(request):
    quiz_type = request.GET.get('type', 'number')
    
    if quiz_type == 'number':
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            answer = num1 + num2
        elif operation == '-':
            answer = num1 - num2
        else:
            answer = num1 * num2
            
        question = f"{num1} {operation} {num2} = ?"
        
    elif quiz_type == 'word':
        words = ['사과', '바나나', '오렌지', '포도', '키위']
        word = random.choice(words)
        answer = word
        question = f"다음 과일의 이름을 입력하세요: {word}"
        
    elif quiz_type == 'time':
        hour = random.randint(1, 12)
        minute = random.randint(0, 59)
        answer = f"{hour:02d}:{minute:02d}"
        question = f"다음 시간을 입력하세요 (HH:MM 형식): {hour}시 {minute}분"
        
    else:  # memory
        sequence = [random.randint(1, 9) for _ in range(4)]
        answer = ''.join(map(str, sequence))
        question = f"다음 숫자들을 순서대로 입력하세요: {' '.join(map(str, sequence))}"
    
    quiz_id = str(uuid.uuid4())
    return JsonResponse({
        'id': quiz_id,
        'question': question,
        'answer': answer
    })

@csrf_exempt
def submit_quiz_answer(request, quiz_id):
    try:
        user_answer = request.POST.get('user_answer')
        if not user_answer:
            return JsonResponse({'error': '답변이 없습니다'}, status=400)
            
        # 실제 구현에서는 quiz_id를 사용하여 저장된 퀴즈를 찾아야 합니다
        # 현재는 간단한 구현을 위해 항상 정답으로 처리
        return JsonResponse({
            'is_correct': True,
            'message': '정답입니다!'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)