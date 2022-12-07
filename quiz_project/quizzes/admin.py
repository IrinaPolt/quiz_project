from django.contrib import admin

from .models import Quiz, Question, Choice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'quiz', 'text', 'question_num')
    list_filter = ('quiz', )
    search_fields = ('quiz__title', 'text')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'amount_questions')
    list_filter = ('title', )

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'question', 'choice_text', 'correct')
    list_filter = ('question', )
    search_fields = ('question__quiz__title', 'question__text') # by far case sensitive



admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
