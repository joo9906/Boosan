from django.db import models
from account.models import User

# Create your models here.
# models.py

class Quiz(models.Model):
    CATEGORY_CHOICES = [
        ('number', '숫자'),
        ('word', '단어'),
        ('memory', '기억'),
        ('time', '시간'),
        ('general', '일반상식'),
        ('season', '계절/이벤트'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', '쉬움'),
        ('medium', '보통'),
        ('hard', '어려움'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    question = models.TextField(verbose_name='문제')
    answer = models.TextField(verbose_name='정답')
    hint = models.TextField(blank=True, null=True, verbose_name='힌트')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 통계 필드
    total_attempts = models.IntegerField(default=0, verbose_name='총 시도 횟수')
    correct_attempts = models.IntegerField(default=0, verbose_name='정답 횟수')
    
    class Meta:
        verbose_name = '퀴즈'
        verbose_name_plural = '퀴즈 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"[{self.get_category_display()}] {self.question[:30]}..."
    
    @property
    def success_rate(self):
        """정답률 계산"""
        if self.total_attempts == 0:
            return 0
        return round((self.correct_attempts / self.total_attempts) * 100, 1)

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    user_answer = models.TextField(verbose_name='사용자 답변')
    is_correct = models.BooleanField(verbose_name='정답 여부')
    attempt_date = models.DateField(auto_now_add=True, verbose_name='시도 날짜')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '퀴즈 결과'
        verbose_name_plural = '퀴즈 결과 목록'
        ordering = ['-created_at']
        # 같은 날 같은 퀴즈는 한 번만 시도 가능
        unique_together = ['user', 'quiz', 'attempt_date']
    
    def __str__(self):
        return f"{self.user.name} - {self.quiz.question[:20]}... ({'정답' if self.is_correct else '오답'})"

class DailyQuizSet(models.Model):
    """일일 퀴즈 세트 관리"""
    date = models.DateField(unique=True, verbose_name='날짜')
    quizzes = models.ManyToManyField(Quiz, verbose_name='선택된 퀴즈들')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '일일 퀴즈 세트'
        verbose_name_plural = '일일 퀴즈 세트 목록'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} 퀴즈 세트 ({self.quizzes.count()}개)"
