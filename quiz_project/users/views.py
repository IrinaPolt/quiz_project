from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from quizzes.models import Quiz

from .forms import CreationForm
from .models import Achievements, QuizInAchievements

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('quizzes:index')
    template_name = 'users/signup.html'


def personal_page(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    achievements = Achievements.objects.get_or_create(user=user)
    results = QuizInAchievements.objects.filter(
        user_achievements=achievements[0])
    context = {
        'user': user,
        'results': results,
    }
    return render(request, 'users/user.html', context)


def delete_result(request, quiz_id):
    achievements = get_object_or_404(Achievements, user=request.user)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    result = get_object_or_404(
        QuizInAchievements,
        quiz=quiz,
        user_achievements=achievements)
    result.delete()
    return render(request, 'users/user.html')
