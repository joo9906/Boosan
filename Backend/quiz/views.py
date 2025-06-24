# quiz/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from datetime import date, timedelta
import random
from .models import Quiz, QuizResult, DailyQuizSet
from .serializers import QuizSerializer, QuizResultSerializer
from .openai_connect import generate_quiz

@api_view(['GET'])
def create_quiz(request):
    quiz_type = request.query_params.get('type', 'number')
    content = generate_quiz(quiz_type)
    
    try:
        question = content.split('문제:')[1].split('정답:')[0].strip()
        answer = content.split('정답:')[1].strip()
    except:
        return Response({'error': 'Quiz parsing error'}, status=500)

    quiz = Quiz.objects.create(question=question, answer=answer)
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@api_view(['POST'])
def submit_answer(request, quiz_id):
    user_answer = request.data.get('user_answer')
    quiz = Quiz.objects.get(id=quiz_id)
    is_correct = (quiz.answer.strip() == user_answer.strip())
    result = QuizResult.objects.create(quiz=quiz, user_answer=user_answer, is_correct=is_correct)
    return Response({'is_correct': is_correct})

@api_view(['GET'])
# @permission_classes([IsAuthenticated])  # 임시로 주석 처리
def get_daily_quiz(request):
    """오늘의 퀴즈 가져오기"""
    today = date.today()
    
    # 임시로 첫 번째 사용자 사용
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    
    if not user:
        return Response({
            'error': '사용자가 없습니다. 먼저 회원가입을 해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 요일별 테마 맵을 함수 시작 부분에 정의
    weekday = today.weekday()  # 0=월요일, 6=일요일
    category_map = {
        0: 'number',    # 월: 숫자
        1: 'memory',    # 화: 기억
        2: 'word',      # 수: 단어
        3: 'time',      # 목: 시간
        4: 'general',   # 금: 일반상식
        5: 'season',    # 토: 계절/이벤트
        6: 'number',    # 일: 숫자
    }
    target_category = category_map[weekday]
    
    try:
        # 오늘의 퀴즈 세트가 있는지 확인
        daily_set, created = DailyQuizSet.objects.get_or_create(date=today)
        
        if created or daily_set.quizzes.count() == 0:
            # 새로운 퀴즈 세트 생성
            daily_set.quizzes.clear()
            
            # 해당 카테고리에서 활성화된 퀴즈 가져오기
            available_quizzes = Quiz.objects.filter(
                category=target_category,
                is_active=True
            ).exclude(
                # 사용자가 오늘 이미 푼 퀴즈 제외
                results__user=user,
                results__attempt_date=today
            )
            
            # 3개의 퀴즈 선택 (난이도 섞어서)
            selected_quizzes = []
            
            # 쉬움 1개
            easy_quiz = available_quizzes.filter(difficulty='easy').order_by('?').first()
            if easy_quiz:
                selected_quizzes.append(easy_quiz)
            
            # 보통 1개
            medium_quiz = available_quizzes.filter(difficulty='medium').exclude(
                id__in=[q.id for q in selected_quizzes]
            ).order_by('?').first()
            if medium_quiz:
                selected_quizzes.append(medium_quiz)
            
            # 어려움 1개
            hard_quiz = available_quizzes.filter(difficulty='hard').exclude(
                id__in=[q.id for q in selected_quizzes]
            ).order_by('?').first()
            if hard_quiz:
                selected_quizzes.append(hard_quiz)
            
            # 부족한 경우 랜덤으로 채우기
            while len(selected_quizzes) < 3:
                remaining = available_quizzes.exclude(
                    id__in=[q.id for q in selected_quizzes]
                ).order_by('?').first()
                if remaining:
                    selected_quizzes.append(remaining)
                else:
                    break
            
            # 퀴즈 세트에 추가
            daily_set.quizzes.set(selected_quizzes)
        
        # 오늘의 퀴즈 반환
        quizzes = daily_set.quizzes.all()
        quiz_data = []
        
        for quiz in quizzes:
            # 사용자가 이미 푼 퀴즈인지 확인
            user_result = QuizResult.objects.filter(
                user=user,
                quiz=quiz,
                attempt_date=today
            ).first()
            
            quiz_data.append({
                'id': quiz.id,
                'category': quiz.get_category_display(),
                'question': quiz.question,
                'hint': quiz.hint,
                'difficulty': quiz.get_difficulty_display(),
                'is_solved': bool(user_result),
                'user_answer': user_result.user_answer if user_result else None,
                'is_correct': user_result.is_correct if user_result else None,
            })
        
        # 카테고리 이름 찾기
        category_display = dict(Quiz.CATEGORY_CHOICES).get(target_category, '일반')
        
        return Response({
            'success': True,
            'date': today.strftime('%Y-%m-%d'),
            'theme': category_display,
            'quizzes': quiz_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        import traceback
        print(f"Error in get_daily_quiz: {e}")
        print(traceback.format_exc())
        return Response({
            'error': f'퀴즈 로드 중 오류 발생: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])  # 임시로 주석 처리
def submit_quiz_answer(request):
    """퀴즈 답안 제출"""
    try:
        quiz_id = request.data.get('quiz_id')
        user_answer = request.data.get('answer', '').strip()
        
        if not quiz_id or not user_answer:
            return Response({
                'error': '퀴즈 ID와 답안이 필요합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        quiz = Quiz.objects.get(id=quiz_id, is_active=True)
        
        # 임시로 첫 번째 사용자 사용
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.first()
        
        if not user:
            return Response({
                'error': '사용자가 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        today = date.today()
        
        # 이미 푼 퀴즈인지 확인
        existing_result = QuizResult.objects.filter(
            user=user,
            quiz=quiz,
            attempt_date=today
        ).first()
        
        if existing_result:
            return Response({
                'error': '오늘 이미 푼 퀴즈입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 정답 확인 (대소문자 무시, 공백 제거)
        correct_answer = quiz.answer.strip().lower()
        user_answer_clean = user_answer.lower()
        is_correct = correct_answer == user_answer_clean
        
        # 결과 저장
        result = QuizResult.objects.create(
            user=user,
            quiz=quiz,
            user_answer=user_answer,
            is_correct=is_correct,
            attempt_date=today
        )
        
        # 퀴즈 통계 업데이트
        quiz.total_attempts += 1
        if is_correct:
            quiz.correct_attempts += 1
        quiz.save()
        
        return Response({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': quiz.answer,
            'user_answer': user_answer,
            'message': '정답입니다! 🎉' if is_correct else f'아쉽네요. 정답은 "{quiz.answer}"입니다.',
        }, status=status.HTTP_200_OK)
        
    except Quiz.DoesNotExist:
        return Response({
            'error': '존재하지 않는 퀴즈입니다.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        import traceback
        print(f"Error in submit_quiz_answer: {e}")
        print(traceback.format_exc())
        return Response({
            'error': f'답안 제출 중 오류 발생: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz_statistics(request):
    """사용자 퀴즈 통계"""
    user = request.user
    
    try:
        # 전체 통계
        total_results = QuizResult.objects.filter(user=user)
        total_attempts = total_results.count()
        correct_attempts = total_results.filter(is_correct=True).count()
        
        # 카테고리별 통계
        category_stats = {}
        for category_code, category_name in Quiz.CATEGORY_CHOICES:
            cat_results = total_results.filter(quiz__category=category_code)
            cat_total = cat_results.count()
            cat_correct = cat_results.filter(is_correct=True).count()
            
            category_stats[category_name] = {
                'total': cat_total,
                'correct': cat_correct,
                'rate': round((cat_correct / cat_total * 100), 1) if cat_total > 0 else 0
            }
        
        # 최근 7일 통계
        week_ago = date.today() - timedelta(days=7)
        recent_results = total_results.filter(attempt_date__gte=week_ago)
        recent_total = recent_results.count()
        recent_correct = recent_results.filter(is_correct=True).count()
        
        return Response({
            'success': True,
            'overall': {
                'total_attempts': total_attempts,
                'correct_attempts': correct_attempts,
                'success_rate': round((correct_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0
            },
            'recent_week': {
                'total_attempts': recent_total,
                'correct_attempts': recent_correct,
                'success_rate': round((recent_correct / recent_total * 100), 1) if recent_total > 0 else 0
            },
            'by_category': category_stats
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'통계 조회 중 오류 발생: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz_by_category(request, category):
    """카테고리별 퀴즈 가져오기"""
    try:
        user = request.user
        today = date.today()
        
        # 해당 카테고리의 활성화된 퀴즈 중 오늘 안 푼 것들
        available_quizzes = Quiz.objects.filter(
            category=category,
            is_active=True
        ).exclude(
            results__user=user,
            results__attempt_date=today
        ).order_by('?')[:5]  # 랜덤으로 5개
        
        quiz_data = []
        for quiz in available_quizzes:
            quiz_data.append({
                'id': quiz.id,
                'category': quiz.get_category_display(),
                'question': quiz.question,
                'hint': quiz.hint,
                'difficulty': quiz.get_difficulty_display(),
            })
        
        return Response({
            'success': True,
            'category': dict(Quiz.CATEGORY_CHOICES)[category],
            'quizzes': quiz_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'퀴즈 조회 중 오류 발생: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
