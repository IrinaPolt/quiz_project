from django.contrib import admin
from django.db.models import Count

from users.models import Achievements, QuizInAchievements

from .models import (Category, Choice, ChoiceInQuestion, Question,
                     QuestionInQuiz, Quiz, QuizInCategory)


class QuizInAchievementsInlineAdmin(admin.TabularInline):
    model = QuizInAchievements


class ChoiceInQuestionInlineAdmin(admin.TabularInline):
    model = ChoiceInQuestion


class QuestionInQuizInlineAdmin(admin.TabularInline):
    model = QuestionInQuiz


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
    list_display = ('pk', 'text', 'question_num')
    search_fields = ('text', )
    inlines = [ChoiceInQuestionInlineAdmin, ]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizInCategoryInlineAdmin, QuestionInQuizInlineAdmin]
    list_display = ('pk', 'title', 'amount_questions')
    list_filter = ('title', )


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


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'choice_text', 'correct')
    list_filter = ('correct', )
