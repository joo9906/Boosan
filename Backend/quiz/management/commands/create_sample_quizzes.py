from django.core.management.base import BaseCommand
from quiz.models import Quiz

class Command(BaseCommand):
    help = '샘플 퀴즈 데이터를 생성합니다'

    def handle(self, *args, **options):
        # 기존 퀴즈 삭제
        Quiz.objects.all().delete()
        
        sample_quizzes = [
            {
                'category': 'number',
                'question': '10 + 5는 얼마인가요?',
                'answer': '15',
                'hint': '10에 5를 더해보세요',
                'difficulty': 'easy'
            },
            {
                'category': 'number',
                'question': '100에서 25를 빼면 얼마인가요?',
                'answer': '75',
                'hint': '100 - 25를 계산해보세요',
                'difficulty': 'medium'
            },
            {
                'category': 'number',
                'question': '7 × 8은 얼마인가요?',
                'answer': '56',
                'hint': '7을 8번 더하거나 8을 7번 더해보세요',
                'difficulty': 'hard'
            },
            {
                'category': 'memory',
                'question': '아침에 일어나서 가장 먼저 하는 일은 무엇인가요?',
                'answer': '세수',
                'hint': '얼굴을 깨끗하게 하는 일이에요',
                'difficulty': 'easy'
            },
            {
                'category': 'memory',
                'question': '김 할머니는 마트에서 사과 3개와 배 2개를 샀습니다. 총 몇 개의 과일을 샀을까요?',
                'answer': '5',
                'hint': '사과와 배를 모두 더해보세요',
                'difficulty': 'medium'
            },
            {
                'category': 'memory',
                'question': '박 할아버지는 오전 10시에 병원에 갔습니다. 누구를 만나러 갔을까요?',
                'answer': '의사',
                'hint': '병원에서 환자를 진료하는 사람이에요',
                'difficulty': 'medium'
            },
            {
                'category': 'word',
                'question': "'ㄱ'으로 시작하는 과일 이름을 말해보세요",
                'answer': '귤',
                'hint': '겨울에 많이 먹는 주황색 과일이에요',
                'difficulty': 'easy'
            },
            {
                'category': 'word',
                'question': "'사랑'의 반대말은 무엇인가요?",
                'answer': '미움',
                'hint': '좋아하지 않는 감정이에요',
                'difficulty': 'medium'
            },
            {
                'category': 'word',
                'question': "'물'과 관련된 단어를 말해보세요 (물고기 제외)",
                'answer': '물병',
                'hint': '물을 담는 용기예요',
                'difficulty': 'medium'
            },
            {
                'category': 'time',
                'question': '하루는 몇 시간인가요?',
                'answer': '24',
                'hint': '24시간제로 생각해보세요',
                'difficulty': 'easy'
            },
            {
                'category': 'time',
                'question': '1년은 몇 개월인가요?',
                'answer': '12',
                'hint': '1월부터 12월까지 세어보세요',
                'difficulty': 'easy'
            },
            {
                'category': 'general',
                'question': '우리나라의 수도는 어디인가요?',
                'answer': '서울',
                'hint': '한강이 흐르는 우리나라의 중심 도시예요',
                'difficulty': 'easy'
            },
            {
                'category': 'general',
                'question': '태극기에는 몇 개의 색깔이 있나요?',
                'answer': '4',
                'hint': '빨강, 파랑, 검정, 흰색이 있어요',
                'difficulty': 'medium'
            },
            {
                'category': 'season',
                'question': '추석에 먹는 대표적인 음식은 무엇인가요?',
                'answer': '송편',
                'hint': '반달 모양의 떡이에요',
                'difficulty': 'easy'
            },
            {
                'category': 'season',
                'question': '크리스마스는 몇 월 몇 일인가요?',
                'answer': '12월 25일',
                'hint': '12월의 마지막 주에 있어요',
                'difficulty': 'easy'
            }
        ]
        
        created_count = 0
        for quiz_data in sample_quizzes:
            quiz = Quiz.objects.create(**quiz_data)
            created_count += 1
            self.stdout.write(f"생성됨: {quiz.question[:30]}...")
        
        self.stdout.write(
            self.style.SUCCESS(f'성공적으로 {created_count}개의 샘플 퀴즈를 생성했습니다!')
        ) 