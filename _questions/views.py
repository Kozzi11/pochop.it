from functools import reduce

from django.contrib.auth import get_user
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from _questions import urls
from _questions.forms import QuestionForm, TagForm, AnswerForm
from _questions.models import Question, Tag, Answer, VoteQuestion, VoteAnswer


def questions(request):
    if 'q' in request.GET:
        search_query = request.GET['q']
    else:
        search_query = None
    return render(request, '_questions/questions.html', {'search_query': search_query})


def questions_grid_data(request):
    # todo vyladit dotaz tak, aby skutecne vracel relevanti vysledky
    offset = int(request.POST['offset'])
    if 'q' in request.GET:
        search_list = request.POST['s'].split(' ')
        question_list = Question.objects.filter(
            reduce(lambda x, y: x | y, [Q(title__contains=item) for item in search_list]))[offset:offset + 10]
    else:
        question_list = Question.objects.all()[offset:offset + 10]

    return render(request, '_questions/question.html', {'question_list': question_list})


def find_tags(request):
    search = request.POST['search']
    tags_alredy_added = filter(None, request.POST['tags'].split(';'))
    tags = Tag.objects.filter(title__contains=search).exclude(id__in=tags_alredy_added)[:10]
    response = ''
    for tag in tags:
        response += '<li onclick="addTag(' + str(tag.id) + ', \'' + tag.title + '\')">' + tag.title + '</li>'
    return HttpResponse(response)


def ask_question(request):
    if request.method == 'POST':
        question = Question()
        question.user = get_user(request)
        form = QuestionForm(request.POST, instance=question)
        form.save()
        added_tags_ids = filter(None, request.POST['added_tags'].split(';'))
        question.tag_set = Tag.objects.filter(id__in=added_tags_ids)
        question.text = form.cleaned_data['text']
        question.save()
        url = reverse(urls.QUESTIONS)
        return HttpResponseRedirect(url)
    else:
        form = QuestionForm()

    return render(request, '_questions/question_form.html', {'form': form})


def view_question(request, question_id):
    question = Question.objects.get(id=question_id)
    user = get_user(request)
    if request.method == 'POST':
        answer = Answer()
        answer.user = user
        answer.question = question
        form = AnswerForm(request.POST, instance=answer)
        form.save()
        # answer.text = form.cleaned_data['text']
        url = reverse(urls.VIEW_QUESTION, args=(question.id,))
        return HttpResponseRedirect(url)
    else:
        question.views += 1
        question.save()
        form = AnswerForm()

    user_aleready_aswered = question.answer_set.filter(user=user).count() > 0
    return render(request, '_questions/question_detail.html',
                  {'question': question, 'form': form, 'user_aleready_aswered': user_aleready_aswered})


def create_tag(request):
    if request.method == 'POST':
        tag = Tag()
        tag.user = get_user(request)
        form = TagForm(request.POST, instance=tag)
        form.save()
        url = reverse(urls.CREATE_TAG)
        return HttpResponseRedirect(url)
    else:
        form = TagForm()

    return render(request, '_questions/tag_form.html', {'form': form})


def vote_up_question(request, question_id):
    user = get_user(request)
    question = Question.objects.get(id=question_id)
    user_not_voted = question.votequestion_set.filter(user=user).count() == 0
    if user_not_voted:
        vote = VoteQuestion()
        vote.user = user
        vote.question = question
        vote.up = True
        vote.save()
        question.votes += 1
        question.save()

    url = reverse(urls.VIEW_QUESTION, args=(question_id,))
    return HttpResponseRedirect(url)


def vote_down_question(request, question_id):
    user = get_user(request)
    question = Question.objects.get(id=question_id)
    user_not_voted = question.votequestion_set.filter(user=user).count() == 0
    if user_not_voted:
        vote = VoteQuestion()
        vote.user = user
        vote.question = question
        vote.up = False
        vote.save()
        question.votes -= 1
        question.save()
    url = reverse(urls.VIEW_QUESTION, args=(question_id,))
    return HttpResponseRedirect(url)


def vote_up_answer(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    user_not_voted = answer.voteanswer_set.filter(user=user).count() == 0
    if user_not_voted:
        vote = VoteAnswer()
        vote.user = user
        vote.answer = answer
        vote.up = True
        vote.save()
        answer.votes += 1
        answer.save()

    url = reverse(urls.VIEW_QUESTION, args=(answer.question_id,))
    return HttpResponseRedirect(url)


def vote_down_answer(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    user_not_voted = answer.voteanswer_set.filter(user=user).count() == 0
    if user_not_voted:
        vote = VoteAnswer()
        vote.user = user
        vote.answer = answer
        vote.up = False
        vote.save()
        answer.votes -= 1
        answer.save()
    url = reverse(urls.VIEW_QUESTION, args=(answer.question_id,))
    return HttpResponseRedirect(url)
