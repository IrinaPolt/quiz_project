from django.db import models


class Quiz(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название')
    amount_questions = models.IntegerField(
        default=0,
        verbose_name='Количество вопросов')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        order = ['-id']

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Тест')
    text = models.CharField(
        max_length=300,
        verbose_name='Текст вопроса')
    question_num = models.IntegerField(
        default=0,
        verbose_name='Номер вопроса')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос')
    choice_text = models.CharField(
        max_length=300,
        verbose_name='Текст ответа')
    correct = models.BooleanField(
        default=False,
        verbose_name='Правильность ответа')

    def __str__(self):
        return self.choice_text
