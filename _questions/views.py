from functools import reduce
from django.contrib import messages

from django.contrib.auth import get_user
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from _messages.models import Message
from _questions.constants import URLS
from _questions.forms import QuestionForm, TagForm, AnswerForm, QuestionRevisionForm, AnswerRevisionForm, \
    QuestionSupervisorRevisionForm, AnswerSupervisorRevisionForm
from _questions.models import Question, Tag, Answer, VoteQuestion, VoteAnswer, QuestionRevision, AnswerRevision, \
    QuestionComment, AnswerComment
from django.utils.translation import ugettext as _
from pochopit.app_util import AppUtil
from pochopit.models import MinuteTransaction


def questions(request):
    if 'q' in request.GET:
        search_query = request.GET['q']
    else:
        search_query = ''
    return render(request, '_questions/questions.html', {'search_query': search_query})


def questions_grid_data(request):
    # todo vyladit dotaz tak, aby skutecne vracel relevanti vysledky
    offset = int(request.POST['offset'])
    if 'q' in request.POST:
        search_list = request.POST['q'].split(' ')
        question_list = Question.objects.filter(
            reduce(lambda x, y: x | y, [Q(title__contains=item) for item in search_list])).order_by('-created')[
                        offset:offset + 10]
    else:
        question_list = Question.objects.all().order_by('-created')[offset:offset + 10]

    return render(request, '_questions/question.html', {'question_list': question_list})


def ask_question(request):
    tags = []
    if request.method == 'POST':
        question = Question()
        question.user = get_user(request)
        added_tags_ids = filter(None, request.POST['added_tags'].split(';'))
        tags = Tag.objects.filter(id__in=added_tags_ids)
        form = QuestionForm(request.POST, instance=question)
        if request.POST['text']:
            form.save()

            question.tag_set = tags
            question.text = form.cleaned_data['text']
            question.save()
            url = reverse(URLS.QUESTIONS)
            return HttpResponseRedirect(url)
        else:
            form.add_error('text', _("Concise description of the problem must be specified"))
    else:
        form = QuestionForm()

    return render(request, '_questions/question_form.html', {'form': form, 'tags': tags})


def view_question(request, question_id, question_title):
    question = Question.objects.get(id=question_id)
    user = get_user(request)

    user_aleready_aswered = question.answer_set.filter(user=user).count() > 0
    if request.method == 'POST':
        answer = Answer()
        answer.user = user
        answer.question = question
        form = AnswerForm(request.POST, instance=answer)
        if user_aleready_aswered:
            messages.add_message(request, messages.ERROR, _('You can add only one answer to question!'))
        else:
            if request.POST['text']:
                form.save()
                message = Message()
                message.user = question.user
                message.sender = user
                message.status = 0
                message.params = question.id
                message.type = Message.TYPE_QUESTION
                message.save()
                url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
                return HttpResponseRedirect(url)
            else:
                form.add_error('text', _("Answer was not filed"))
    else:
        question.views += 1
        question.save()
        form = AnswerForm()

    return render(request, '_questions/question_detail.html',
                  {'question': question, 'form': form, 'user_aleready_aswered': user_aleready_aswered})


def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    tags = question.tag_set.all()
    question_revision = QuestionRevision()
    question_revision.question = question
    question_revision.editor = get_user(request)
    question_revision.title = question.title
    question_revision.text = question.text
    if request.method == 'POST':
        form = QuestionRevisionForm(request.POST, instance=question_revision)
        added_tags_ids = filter(None, request.POST['added_tags'].split(';'))
        tags = Tag.objects.filter(id__in=added_tags_ids)
        if request.POST['text']:
            form.save()
            question_revision.tags = tags
            question_revision.text = form.cleaned_data['text']
            question_revision.save()
            url = reverse(URLS.QUESTIONS)
            return HttpResponseRedirect(url)
        else:
            form.add_error('text', _("Concise description of the problem must be specified"))
    else:
        form = QuestionRevisionForm(instance=question_revision)

    return render(request, '_questions/question_revision.html',
                  {'form': form, 'tags': tags, 'question': question})


def check_question_revision(request, question_id):
    question = Question.objects.get(id=question_id)
    revision = question.questionrevision_set.filter(status=QuestionRevision.STATUS_AWATING_APPROVAL).order_by(
        'created')[:1][0]
    if request.method == 'POST':
        revision_id = request.POST['revision_id']
        if int(revision_id) == revision.id:
            supervisor = get_user(request)
            revision.status = QuestionRevision.STATUS_APPROVED
            revision.supervisor = supervisor
            question.title = revision.title
            question.text = revision.text

            added_tags_ids = filter(None, request.POST['added_tags'].split(';'))
            tags = Tag.objects.filter(id__in=added_tags_ids)
            question.tag_set = tags
            question.save()
            revision.save()
            context_info = 'question_id:' + str(question.id) + ';' + 'revision_id:' + str(revision.id)
            system_user = AppUtil.get_system_user()
            AppUtil.process_transaction(user_from=system_user, user_to=supervisor,
                                        amount=MinuteTransaction.AMOUNT_APPROVE_QUESTION_EDIT,
                                        trans_type=MinuteTransaction.TYPE_APPROVE_QUESTION_EDIT,
                                        context_info=context_info)

            amount = 0
            sophistication = request.POST['sophistication']
            if sophistication == '1':
                amount = MinuteTransaction.AMOUNT_EDIT_QUESTION_SMALL
            elif sophistication == '2':
                amount = MinuteTransaction.AMOUNT_EDIT_QUESTION_MIDDLE
            elif sophistication == '3':
                amount = MinuteTransaction.AMOUNT_EDIT_QUESTION_FULL

            AppUtil.process_transaction(user_from=system_user, user_to=revision.editor,
                                        amount=amount,
                                        trans_type=MinuteTransaction.TYPE_EDIT_QUESTION,
                                        context_info=context_info)
            url = reverse(URLS.QUESTIONS)
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _('Revision already approved'))

    revision_form = QuestionSupervisorRevisionForm(instance=revision)
    tags = revision.tags.all()

    return render(request, '_questions/question_revision.html',
                  {'question': question, 'revision': revision, 'form': revision_form, 'tags': tags})


def question_add_comment(request):
    question_id = request.POST['id']
    commnet_text = request.POST['comment']
    question = Question.objects.get(id=question_id)

    comment = QuestionComment()
    comment.user = get_user(request)
    comment.text = commnet_text
    comment.question = question
    comment.save()
    return HttpResponse('')


def edit_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question = answer.question

    answer_revision = AnswerRevision()
    answer_revision.answer = answer
    answer_revision.editor = get_user(request)
    answer_revision.text = answer.text
    if request.method == 'POST':
        form = AnswerRevisionForm(request.POST, instance=answer_revision)
        if request.POST['text']:
            form.save()
            answer_revision.text = form.cleaned_data['text']
            answer_revision.save()
            url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
            return HttpResponseRedirect(url)
        else:
            form.add_error('text', _("Answer was not filed"))
    else:
        form = AnswerRevisionForm(instance=answer_revision)

    return render(request, '_questions/answer_revision.html', {'form': form, 'question': question, 'answer': answer})


def check_answer_revision(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    revision = answer.answerrevision_set.filter(status=AnswerRevision.STATUS_AWATING_APPROVAL).order_by(
        'created')[:1][0]
    if request.method == 'POST':
        revision_id = request.POST['revision_id']
        if int(revision_id) == revision.id:
            supervisor = get_user(request)
            revision.status = AnswerRevision.STATUS_APPROVED
            revision.supervisor = supervisor
            answer.text = revision.text
            answer.save()
            revision.save()
            context_info = 'answer_id:' + str(answer.id) + ';' + 'revision_id:' + str(revision.id)
            system_user = AppUtil.get_system_user()
            AppUtil.process_transaction(user_from=system_user, user_to=supervisor,
                                        amount=MinuteTransaction.AMOUNT_APPROVE_ANSWER_EDIT,
                                        trans_type=MinuteTransaction.TYPE_APPROVE_ANSWER_EDIT,
                                        context_info=context_info)

            amount = 0
            sophistication = request.POST['sophistication']
            if sophistication == '1':
                amount = MinuteTransaction.AMOUNT_EDIT_ANSWER_SMALL
            elif sophistication == '2':
                amount = MinuteTransaction.AMOUNT_EDIT_ANSWER_MIDDLE
            elif sophistication == '3':
                amount = MinuteTransaction.AMOUNT_EDIT_ANSWER_FULL

            AppUtil.process_transaction(user_from=system_user, user_to=revision.editor,
                                        amount=amount,
                                        trans_type=MinuteTransaction.TYPE_EDIT_ANSWER,
                                        context_info=context_info)
            url = reverse(URLS.QUESTIONS)
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _('Revision already approved'))

    form = AnswerSupervisorRevisionForm(instance=revision)
    return render(request, '_questions/answer_revision.html',
                  {'question': answer.question, 'answer': answer, 'revision': revision, 'form': form})


def answer_add_comment(request):
    answer_id = request.POST['id']
    commnet_text = request.POST['comment']
    answer = Answer.objects.get(id=answer_id)

    comment = AnswerComment()
    comment.user = get_user(request)
    comment.text = commnet_text
    comment.answer = answer
    comment.save()
    return HttpResponse('')


def vote_up_question(request, question_id):
    user = get_user(request)
    question = Question.objects.get(id=question_id)
    user_not_voted = question.votequestion_set.filter(user=user).count() == 0
    if user_not_voted:
        vote = VoteQuestion()
        vote.user = user
        vote.up = True
        vote.question = question

        votequestion_set = question.votequestion_set.filter(minutes__lt=MinuteTransaction.MAX_AMOUNT_VOTE_QUESTION)
        for votequestion in votequestion_set:
            user_from = AppUtil.get_system_user()
            user_to = votequestion.user
            votequestion.minutes += MinuteTransaction.AMOUNT_VOTE_QUESTION
            context_info = 'question_id:' + str(question.id) + ';' + 'vote_id:' + str(vote.id)
            AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                        amount=MinuteTransaction.AMOUNT_VOTE_QUESTION,
                                        trans_type=MinuteTransaction.TYPE_VOTE_QUESTION, context_info=context_info)
            votequestion.save()

        vote.save()
        question.votes += 1
        if question.paid is False and question.votes == MinuteTransaction.VOTE_COUNT_ADD_QUESTION:
            user_from = AppUtil.get_system_user()
            user_to = question.user
            question.paid = True
            context_info = 'question_id:' + str(question.id) + ';' + 'vote_id:' + str(vote.id)
            AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                        amount=MinuteTransaction.AMOUNT_ADD_QUESTION,
                                        trans_type=MinuteTransaction.TYPE_ADD_QUESTION, context_info=context_info)
        question.save()

    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
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
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    return HttpResponseRedirect(url)


def vote_up_answer(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    question = answer.question

    user_not_voted = VoteAnswer.objects.filter(user=user, answer__in=question.answer_set.all()).count() == 0
    if user_not_voted:
        vote = VoteAnswer()
        vote.user = user
        vote.answer = answer
        vote.up = True

        voteanser_set = answer.voteanswer_set.filter(minutes__lt=MinuteTransaction.MAX_AMOUNT_VOTE_ANSWER)
        for voteanswer in voteanser_set:
            user_from = AppUtil.get_system_user()
            user_to = voteanswer.user
            voteanswer.minutes += MinuteTransaction.AMOUNT_VOTE_ANSWER
            context_info = 'answer_id:' + str(answer.id) + ';' + 'vote_id:' + str(vote.id)
            AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                        amount=MinuteTransaction.AMOUNT_VOTE_ANSWER,
                                        trans_type=MinuteTransaction.TYPE_VOTE_ANSWER, context_info=context_info)
            voteanswer.save()

        vote.save()
        answer.votes += 1
        if answer.paid is False and answer.votes == MinuteTransaction.VOTE_COUNT_ADD_ANSWR:
            user_from = AppUtil.get_system_user()
            user_to = answer.user
            answer.paid = True
            context_info = 'answer_id:' + str(answer.id) + ';' + 'vote_id:' + str(vote.id)
            AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                        amount=MinuteTransaction.AMOUNT_ADD_ANSWER,
                                        trans_type=MinuteTransaction.TYPE_ADD_ANSWER, context_info=context_info)
        answer.save()

    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    return HttpResponseRedirect(url)


def vote_down_answer(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    question = answer.question

    user_not_voted = VoteAnswer.objects.filter(user=user, answer__in=question.answer_set.all()).count() == 0
    if user_not_voted:
        vote = VoteAnswer()
        vote.user = user
        vote.answer = answer
        vote.up = False
        vote.save()
        answer.votes -= 1
        answer.save()

    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    return HttpResponseRedirect(url)


def create_tag(request):
    if request.method == 'POST':
        tag = Tag()
        tag.user = get_user(request)
        form = TagForm(request.POST, instance=tag)
        form.save()
        url = reverse(URLS.CREATE_TAG)
        return HttpResponseRedirect(url)
    else:
        form = TagForm()

    return render(request, '_questions/tag_form.html', {'form': form})


def find_tags(request):
    search = request.POST['search']
    tags_alredy_added = filter(None, request.POST['tags'].split(';'))
    tags = Tag.objects.filter(title__contains=search).exclude(id__in=tags_alredy_added)[:10]
    response = ''
    for tag in tags:
        response += '<li onclick="addTag(' + str(tag.id) + ', \'' + tag.title + '\')">' + tag.title + '</li>'
    return HttpResponse(response)
