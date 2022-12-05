from django import forms


class QuizForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label='Название теста',
        widget=forms.TextInput(attrs={'class': 'quiz_name_box'})
    )
    amount_questions = forms.IntegerField(
        label='Количество вопросов',
        widget=forms.NumberInput(attrs={'class': 'num_questions_box'})
    )


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
