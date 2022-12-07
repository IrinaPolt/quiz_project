from django.contrib import admin
from django.db.models import Count

from .models import Quiz, Question, Choice, Category, QuizInCategory

from users.models import Achievements, QuizInAchievements


class QuizInAchievementsInlineAdmin(admin.TabularInline):
    model = QuizInAchievements


@admin.register(Achievements)
class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_quizzes_count')
    search_fields = ('user', 'quizzes__quiz__title')
    inlines = [QuizInAchievementsInlineAdmin, ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(quizzes_count=Count('quizinachievements'))
    
    @staticmethod
    def get_quizzes_count(obj):
        return obj.quizzes_count


class QuizInCategoryInlineAdmin(admin.TabularInline):
    model = QuizInCategory


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'quiz', 'text', 'question_num')
    list_filter = ('quiz', )
    search_fields = ('quiz__title', 'text')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizInCategoryInlineAdmin, ]
    list_display = ('pk', 'title', 'amount_questions')
    list_filter = ('title', )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'choice_text', 'correct')
    list_filter = ('question', )
    search_fields = ('question__quiz__title', 'question__text') # by far case sensitive


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_quizzes_count')
    search_fields = ('title', 'quiz__title')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(quizzes_count=Count('quizincategory'))
    
    @staticmethod
    def get_quizzes_count(obj):
        return obj.quizzes_count
