from django import forms
from django.core.exceptions import ValidationError

from .models import Quiz


class QuizForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        label='Название теста',
        widget=forms.TextInput(attrs={'class': 'quiz_name_box'})
    )
    amount_questions = forms.IntegerField(
        label='Количество вопросов',
        widget=forms.NumberInput(attrs={'class': 'num_questions_box'})
    )

    class Meta:
        model = Quiz
        fields = ['title', 'amount_questions']


class QuestionForm(forms.Form):
    text = forms.CharField(
        max_length=300,
        label='Текст вопроса',
        widget=forms.TextInput(attrs={'class': 'question_text_box'})
    )

    choice1_text = forms.CharField(
        max_length=300,
        label='Первый вариант ответа',
        widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice1_correctness = forms.BooleanField(
        label='Это правильный ответ?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'})
    )

    choice2_text = forms.CharField(
        max_length=300,
        label='Второй вариант ответа',
        widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice2_correctness = forms.BooleanField(
        label='Это правильный ответ?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'})
    )

    choice3_text = forms.CharField(
        max_length=300,
        label='Третий вариант ответа',
        widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice3_correctness = forms.BooleanField(
        label='Это правильный ответ?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'})
    )

    choice4_text = forms.CharField(
        max_length=300,
        label='Четвертый вариант ответа',
        widget=forms.TextInput(attrs={'class': 'choice_box'}))
    choice4_correctness = forms.BooleanField(
        label='Это правильный ответ?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'choice_correct_box'})
    )

    def clean(self):
        answer_list = [
            self.cleaned_data['choice1_correctness'],
            self.cleaned_data['choice2_correctness'],
            self.cleaned_data['choice3_correctness'],
            self.cleaned_data['choice4_correctness']]

        right = 0
        for answer in answer_list:
            if answer is True:
                right += 1

        if right > 1:
            raise ValidationError('Должен быть 2+ правильный вариант ответа')
        return self.cleaned_data
