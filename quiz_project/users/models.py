from django.db import models
from django.contrib.auth import get_user_model

from quizzes.models import Quiz

User = get_user_model()


class Achievements(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    quizzes = models.ManyToManyField(
        Quiz,
        through='QuizInAchievements',
        verbose_name='Пройденные тесты',
        blank=True
    )

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return f'Достижения {self.user.username}'


class QuizInAchievements(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.DO_NOTHING,
        verbose_name='Тест'
    )
    user_achievements = models.ForeignKey(
        Achievements,
        on_delete=models.CASCADE,
        verbose_name='Достижения'
    )
    result = models.CharField(
        max_length=10,
        verbose_name='Процент выполнения'
    )

    class Meta:
        verbose_name = 'Пройденный тест'
        verbose_name_plural = 'Пройденные тесты'

    def __str__(self):
        return f'Тест {self.quiz.title} выполнен на {self.result}'
