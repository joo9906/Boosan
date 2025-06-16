# quiz/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Quiz, QuizResult
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
