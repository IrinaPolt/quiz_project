from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Quiz, Question, Choice

from .forms import QuizForm, QuestionForm


def index(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes,
    }
    return render(request, 'quizzes/index.html', context)


def single_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    request.session['amount_correct'] = 0
    request.session['amount_wrong'] = 0
    amount_questions = len(quiz.question_set.all())
    context = {
        'quiz': quiz,
        'amount_questions': amount_questions,
    }
    return render(request, 'quizzes/single_quiz.html', context)


def single_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(question_num=question_id)
    next_or_submit = 'Далее'
    last_question_check = False
    if question_id == (len(quiz.question_set.all())):
        last_question_check = True
        next_or_submit = 'Завершить тест'

    next_question_id = question_id+1
    all_choices = current_question.choice_set.all()
    context = {
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
    current_question = quiz.question_set.get(question_num=question_id)
    next_or_submit = 'Далее'
    if question_id == (len(quiz.question_set.all())):
        next_or_submit = 'Завершить тест'
    try:
        selected_choice = current_question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'quizzes/single_question.html', {
            'quiz': quiz,
            'current_question': current_question,
            'error_message': 'Выберите как минимум один вариант ответа',
            'next_or_submit': next_or_submit,
        })
    else:
        correct_answer = current_question.choice_set.get(correct=True)
        if selected_choice == correct_answer:
            request.session['amount_correct'] += 1
        else:
            request.session['amount_wrong'] += 1
        request.session[str(question_id) + 'selected'] = str(selected_choice)
        request.session[str(question_id) + 'correct'] = str(correct_answer)
        if question_id == (len(quiz.question_set.all())):
            return HttpResponseRedirect(reverse('quizzes:results', args=(quiz.id,)))
        else :
            return HttpResponseRedirect(reverse('quizzes:single_question', args=(quiz.id, question_id+1,)))


def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz_id)
    data = {} # вопросы для вывода
    answers_correct = [] # правильные ответы для вывода
    answers_given = [] # ответы пользователя для вывода
    num = 0
    for question in questions:
        num += 1
        current_question = quiz.question_set.get(question_num=num)
        all_choices = current_question.choice_set.all()
        data[str(num) + '. ' + question.text] = [str(item) for item in all_choices]
        answers_correct.append(request.session[str(num) + 'correct'])
        answers_given.append(request.session[str(num) + 'selected'])
    amount_correct = request.session['amount_correct']
    amount_wrong = request.session['amount_wrong']
    total = amount_correct + amount_wrong
    accuracy = amount_correct / total
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
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return HttpResponseRedirect(reverse('quizzes:create_question', args=(quiz.id, 1,)))
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

            choice1 = form.cleaned_data['choice1_text']
            choice1_correctness = form.cleaned_data['choice1_correctness']

            choice2 = form.cleaned_data['choice2_text']
            choice2_correctness = form.cleaned_data['choice2_correctness']

            choice3 = form.cleaned_data['choice3_text']
            choice3_correctness = form.cleaned_data['choice3_correctness']

            choice4 = form.cleaned_data['choice4_text']
            choice4_correctness = form.cleaned_data['choice4_correctness']

            question = Question(quiz=quiz, text=text, question_num=question_id)
            question.save()

            question.choice_set.create(choice_text=choice1, correct=choice1_correctness)
            question.choice_set.create(choice_text=choice2, correct=choice2_correctness)
            question.choice_set.create(choice_text=choice3, correct=choice3_correctness)
            question.choice_set.create(choice_text=choice4, correct=choice4_correctness)

            if question_id == quiz.amount_questions:
                return HttpResponseRedirect(reverse('quizzes:index'))
            else:
                return HttpResponseRedirect(reverse('quizzes:create_question', args=(quiz_id, question_id+1,)))

    else:
        form = QuestionForm()

    if question_id == quiz.amount_questions:
        next_submit = 'Добавить тест'
    else :
        next_submit = 'Далее'

    context = {
        'form': form,
        'question_num': question_id,
        'next_submit': next_submit,

    }

    return render(request, 'quizzes/create_question.html', context)
