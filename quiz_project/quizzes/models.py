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

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Название категории'
    )
    quizzes = models.ManyToManyField(
        Quiz,
        through='QuizInCategory',
        verbose_name='Тесты в категории'
    )
    slug = models.SlugField(
        max_length=15,
        unique=True,
        verbose_name='Идентификатор')
    description = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Описание категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class QuizInCategory(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тест в категории'
        verbose_name_plural = 'Тесты в категории'


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

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

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

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.choice_text
