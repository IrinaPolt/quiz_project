from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from users.models import Achievements, QuizInAchievements

from .forms import QuestionForm, QuizForm
from .models import (Category, Choice, ChoiceInQuestion, Question,
                     QuestionInQuiz, Quiz, QuizInCategory)


def index(request):
    quizzes = Quiz.objects.all()
    categories = Category.objects.all
    context = {
        'quizzes': quizzes,
        'categories': categories,
    }
    return render(request, 'quizzes/index.html', context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    quizzes = QuizInCategory.objects.filter(category=category)
    context = {
        'category': category,
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/category.html', context)


def single_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    request.session['amount_correct'] = 0
    request.session['amount_wrong'] = 0
    amount_questions = quiz.amount_questions
    context = {
        'quiz': quiz,
        'amount_questions': amount_questions,
    }
    return render(request, 'quizzes/single_quiz.html', context)


def single_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = QuestionInQuiz.objects.filter(quiz=quiz)
    current_question = questions[question_id - 1]
    next_or_submit = 'Далее'
    last_question_check = False
    if question_id == (len(questions)):
        last_question_check = True
        next_or_submit = 'Завершить тест'

    next_question_id = question_id+1
    all_choices = current_question.question.choices.all()
    context = {
        'question_id': question_id,
        'current_question': current_question,
        'all_choices': all_choices,
        'quiz': quiz,
        'next_question_id': next_question_id,
        'last_question_check': last_question_check,
        'next_or_submit': next_or_submit
    }
    return render(request, 'quizzes/single_question.html', context)


def answer(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = QuestionInQuiz.objects.filter(quiz=quiz)
    current_question = questions[question_id - 1]
    next_or_submit = 'Далее'
    if question_id == (len(questions)):
        next_or_submit = 'Завершить тест'
    try:
        selected_choice = current_question.question.choices.get(
            pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'quizzes/single_question.html', {
            'quiz': quiz,
            'current_question': current_question,
            'error_message': 'Выберите как минимум один вариант ответа',
            'next_or_submit': next_or_submit,
        })
    else:
        correct_answer = current_question.question.choices.get(correct=True)
        if selected_choice == correct_answer:
            request.session['amount_correct'] += 1
        else:
            request.session['amount_wrong'] += 1
        request.session[str(question_id) + 'selected'] = str(selected_choice)
        request.session[str(question_id) + 'correct'] = str(correct_answer)
        if question_id == (len(questions)):
            return HttpResponseRedirect(reverse(
                'quizzes:results', args=(quiz.id,)))
        else:
            return HttpResponseRedirect(reverse(
                'quizzes:single_question', args=(quiz.id, question_id+1,)))


def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = QuestionInQuiz.objects.filter(quiz=quiz)
    data = {}  # вопросы для вывода
    answers_correct = []  # правильные ответы для вывода
    answers_given = []  # ответы пользователя для вывода
    num = 0
    for question in questions:
        num += 1
        all_choices = question.question.choices.all()
        data[str(num) + '. ' + question.question.text] = [
            str(item) for item in all_choices]
        answers_correct.append(request.session[str(num) + 'correct'])
        answers_given.append(request.session[str(num) + 'selected'])
    amount_correct = request.session['amount_correct']
    amount_wrong = request.session['amount_wrong']
    total = amount_correct + amount_wrong
    accuracy = amount_correct / total
    request.session['result'] = accuracy
    context = {
        'amount_correct': amount_correct,
        'amount_wrong': amount_wrong,
        'accuracy': '{:.0%}'.format(accuracy),
        'total': total,
        'quiz': quiz,
        'data': data,
        'answers_correct': answers_correct,
        'answers_given': answers_given,
    }
    return render(request, 'quizzes/results.html', context)


@login_required
def choose_category(request, quiz_id):
    categories = Category.objects.all()
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    context = {
        'categories': categories,
        'quiz': quiz,
    }
    return render(request, 'quizzes/categories.html', context)


@login_required
def add_to_category(request, quiz_id, category_id):
    category = get_object_or_404(Category, pk=category_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    QuizInCategory.objects.get_or_create(quiz=quiz, category=category)
    return HttpResponseRedirect(reverse('quizzes:index'))


@login_required
def add_results(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    achievements = Achievements.objects.get_or_create(user=request.user)
    obj, created = QuizInAchievements.objects.update_or_create(
        defaults={'result': '{:.0%}'.format(request.session['result'])},
        quiz=quiz,
        user_achievements=achievements[0],
    )
    return HttpResponseRedirect(reverse('users:me', args=(user.pk,)))


@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return HttpResponseRedirect(
                reverse('quizzes:create_question', args=(quiz.id, 1,)))
    else:
        form = QuizForm()
    context = {
        'form': form,
    }
    return render(request, 'quizzes/create_quiz.html', context)


def create_question(request, quiz_id, question_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            text = form.data['text']
            question = Question.objects.create(
                text=text,
                question_num=question_id)

            choice1_text = form.cleaned_data['choice1_text']
            choice1_correctness = form.cleaned_data['choice1_correctness']
            choice1 = Choice.objects.create(
                choice_text=choice1_text,
                correct=choice1_correctness)
            ChoiceInQuestion.objects.create(question=question, choice=choice1)

            choice2_text = form.cleaned_data['choice2_text']
            choice2_correctness = form.cleaned_data['choice2_correctness']
            choice2 = Choice.objects.create(
                choice_text=choice2_text,
                correct=choice2_correctness)
            ChoiceInQuestion.objects.create(question=question, choice=choice2)

            choice3_text = form.cleaned_data['choice3_text']
            choice3_correctness = form.cleaned_data['choice3_correctness']
            choice3 = Choice.objects.create(
                choice_text=choice3_text,
                correct=choice3_correctness)
            ChoiceInQuestion.objects.create(question=question, choice=choice3)

            choice4_text = form.cleaned_data['choice4_text']
            choice4_correctness = form.cleaned_data['choice4_correctness']
            choice4 = Choice.objects.create(
                choice_text=choice4_text,
                correct=choice4_correctness)
            ChoiceInQuestion.objects.create(question=question, choice=choice4)

            quiz.questions.add(question)

            if question_id == quiz.amount_questions:
                return HttpResponseRedirect(reverse('quizzes:index'))
            else:
                return HttpResponseRedirect(
                    reverse(
                        'quizzes:create_question',
                        args=(quiz_id, question_id+1,)))
        else:
            if question_id == quiz.amount_questions:
                next_submit = 'Добавить тест'
            else:
                next_submit = 'Далее'
            context = {
                'form': form,
                'question_num': question_id,
                'next_submit': next_submit,
            }
            return render(request, 'quizzes/create_question.html', context)

    else:
        form = QuestionForm()

    if question_id == quiz.amount_questions:
        next_submit = 'Добавить тест'
    else:
        next_submit = 'Далее'
    context = {
        'form': form,
        'question_num': question_id,
        'next_submit': next_submit,
    }
    return render(request, 'quizzes/create_question.html', context)
