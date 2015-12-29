from django.contrib.auth import get_user
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from _questions import urls
from _questions.forms import QuestionForm, TagForm
from _questions.models import Question, Tag


def questions(request):
    return render(request, '_questions/questions.html')


def questions_grid_data(request):
    return render(request, '_questions/question.html')


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
        question.text = form.cleaned_data['text']
        question.save()
        url = reverse(urls.QUESTIONS)
        return HttpResponseRedirect(url)
    else:
        form = QuestionForm()

    return render(request, '_questions/question_form.html', {'form': form})


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
