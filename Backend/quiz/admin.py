from django.contrib import admin
from .models import Quiz, QuizResult, DailyQuizSet

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'difficulty', 'is_active', 'success_rate', 'total_attempts', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'category', 'difficulty']
    ordering = ['-created_at']
    
    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = '문제'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('category', 'difficulty', 'is_active')
        }),
        ('문제 내용', {
            'fields': ('question', 'answer', 'hint')
        }),
        ('통계 (읽기 전용)', {
            'fields': ('total_attempts', 'correct_attempts'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['total_attempts', 'correct_attempts']

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz_preview', 'user_answer', 'is_correct', 'attempt_date']
    list_filter = ['is_correct', 'attempt_date', 'quiz__category']
    search_fields = ['user__name', 'quiz__question', 'user_answer']
    readonly_fields = ['user', 'quiz', 'user_answer', 'is_correct', 'attempt_date', 'created_at']
    
    def quiz_preview(self, obj):
        return obj.quiz.question[:30] + "..." if len(obj.quiz.question) > 30 else obj.quiz.question
    quiz_preview.short_description = '퀴즈'
    
    def has_add_permission(self, request):
        return False  # 결과는 직접 추가하지 않음

@admin.register(DailyQuizSet)
class DailyQuizSetAdmin(admin.ModelAdmin):
    list_display = ['date', 'quiz_count', 'created_at']
    filter_horizontal = ['quizzes']
    ordering = ['-date']
    
    def quiz_count(self, obj):
        return obj.quizzes.count()
    quiz_count.short_description = '퀴즈 개수'
