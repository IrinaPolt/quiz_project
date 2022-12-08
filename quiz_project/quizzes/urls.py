from django.urls import path

from . import views

app_name = 'quizzes'


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:slug>/', views.category, name='category'),
    path('category/<int:category_id>/<int:quiz_id>/', views.add_to_category, name='add_to_category'),
    path('categories/<int:quiz_id>/', views.choose_category, name='choose_category'),
    path('<int:quiz_id>/', views.single_quiz, name='single_quiz'),
    path('<int:quiz_id>/<int:question_id>/', views.single_question, name='single_question'),
    path('<int:quiz_id>/<int:question_id>/answer/', views.answer, name='answer'),
    path('<int:quiz_id>/results/add/', views.add_results, name='add_achievement'),
    path('<int:quiz_id>/results/', views.results, name='results'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('create/<int:quiz_id>/<int:question_id>/', views.create_question, name='create_question'),
]
