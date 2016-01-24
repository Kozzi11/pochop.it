from functools import reduce
import datetime
from django.contrib import messages

from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from _messages.models import Message
from _messages.utils import MessageUtil
from _questions.constants import URLS, PERMISSION, PERMISSION_GROUPS
from _questions.forms import QuestionForm, TagForm, AnswerForm, QuestionRevisionForm, AnswerRevisionForm, \
    QuestionSupervisorRevisionForm, AnswerSupervisorRevisionForm
from _questions.models import Question, Tag, Answer, VoteQuestion, VoteAnswer, QuestionRevision, AnswerRevision, \
    QuestionComment, AnswerComment, QuestionScrap, AnswerScrap, AnswerCommentScrap, QuestionCommentScrap
from django.utils.translation import ugettext as _
from pochopit.app_util import AppUtil
from pochopit.models import MitTransaction

QUESTION_SCRAP_LIMIT = 5
ANSWER_SCRAP_LIMIT = QUESTION_SCRAP_LIMIT


def questions(request):
    if 'q' in request.GET:
        search_query = request.GET['q']
    else:
        search_query = ''

    if request.user.is_authenticated():
        user_is_supervisor = get_user(request).groups.filter(name=PERMISSION_GROUPS.SUPERVISOR).exists()
    else:
        user_is_supervisor = False

    return render(request, '_questions/questions.html',
                  {'search_query': search_query, 'user_is_supervisor': user_is_supervisor})


def questions_grid_data(request):
    # todo vyladit dotaz tak, aby skutecne vracel relevanti vysledky
    offset = int(request.POST['offset'])
    if 'q' in request.POST:
        search_list = request.POST['q'].split(' ')
        question_list = Question.objects.filter(
            reduce(lambda x, y: x | y, [Q(title__contains=item) for item in search_list])).exclude(
            scrap__gt=5).order_by('-created')[offset:offset + 10]
    else:
        question_list = Question.objects.exclude(scrap__gt=QUESTION_SCRAP_LIMIT).order_by('-created')[
                        offset:offset + 10]

    return render(request, '_questions/question.html', {'question_list': question_list})


@login_required
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
    show_answer_input = False

    if request.user.is_authenticated():
        show_answer_input = question.user_id != user.id and question.answer_set.filter(user=user).count() == 0

    if request.user.is_authenticated() and request.method == 'POST':
        answer = Answer()
        answer.user = user
        answer.question = question
        form = AnswerForm(request.POST, instance=answer)
        if show_answer_input is False:
            messages.add_message(request, messages.ERROR, _('You can add only one answer to question!'))
        else:
            if request.POST['text']:
                form.save()
                MessageUtil.send_message(user, question.user, Message.TYPE_NEW_ANSWER, params=question.id)
                url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
                return HttpResponseRedirect(url)
            else:
                form.add_error('text', _("Answer was not filed"))
    else:
        question.views += 1
        question.save()
        form = AnswerForm()

    answer_set = question.answer_set.exclude(scrap__gt=ANSWER_SCRAP_LIMIT)
    auth_question_edit = user.has_perm(PERMISSION.AUTHORIZE_QUESTION_EDIT)
    auth_answer_edit = user.has_perm(PERMISSION.AUTHORIZE_ANSWER_EDIT)
    return render(request, '_questions/question_detail.html',
                  {'question': question, 'form': form, 'show_answer_input': show_answer_input, 'answer_set': answer_set,
                   'authorize_question_edit': auth_question_edit, 'authorize_answer_edit': auth_answer_edit})


@login_required
def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    tags = question.tag_set.all()
    prev_revision = None

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
        if question.questionrevision_set \
                .filter(status=QuestionRevision.STATUS_AWATING_APPROVAL).count() > 0:

            prev_revision = question.questionrevision_set \
                                .filter(status=QuestionRevision.STATUS_AWATING_APPROVAL).order_by('-created')[:1][0]
            form = QuestionRevisionForm(instance=prev_revision)
            form.initial['editor_comment'] = ''
            tags = prev_revision.tags.all()
        else:
            form = QuestionRevisionForm(instance=question_revision)

    return render(request, '_questions/question_revision.html',
                  {'form': form, 'tags': tags, 'question': question, 'prev_revision': prev_revision})


@login_required
@permission_required(PERMISSION.AUTHORIZE_QUESTION_EDIT)
def authorize_question_edit(request, question_id):
    question = Question.objects.get(id=question_id)
    supervisor = get_user(request)
    revision = question.questionrevision_set.filter(status=QuestionRevision.STATUS_AWATING_APPROVAL).exclude(
        editor=supervisor).order_by('created')[:1][0]

    if not revision:
        messages.add_message(request, messages.WARNING, _('Nothing to review!'))
        return HttpResponseRedirect(URLS.QUESTIONS)

    if request.method == 'POST':
        revision_id = request.POST['revision_id']
        if int(revision_id) == revision.id:
            url = reverse(URLS.QUESTIONS)
            if 'not-approve' in request.POST:
                revision.status = QuestionRevision.STATUS_REJECTED
                revision.supervisor = supervisor
                revision.editor_comment = request.POST['editor_comment']
                revision.save()
                MessageUtil.send_message(supervisor, revision.editor, Message.TYPE_QUESTION_EDIT_DENIED,
                                         params=revision.id)
                return HttpResponseRedirect(url)

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
                                        amount=MitTransaction.AMOUNT_APPROVE_QUESTION_EDIT,
                                        trans_type=MitTransaction.TYPE_APPROVE_QUESTION_EDIT,
                                        context_info=context_info)

            amount = 0
            sophistication = request.POST['sophistication']
            if sophistication == '1':
                amount = MitTransaction.AMOUNT_EDIT_QUESTION_SMALL
            elif sophistication == '2':
                amount = MitTransaction.AMOUNT_EDIT_QUESTION_MIDDLE
            elif sophistication == '3':
                amount = MitTransaction.AMOUNT_EDIT_QUESTION_FULL

            AppUtil.process_transaction(user_from=system_user, user_to=revision.editor,
                                        amount=amount,
                                        trans_type=MitTransaction.TYPE_EDIT_QUESTION,
                                        context_info=context_info)

            MessageUtil.send_message(supervisor, revision.editor, Message.TYPE_QUESTION_EDIT_AUTHORIZED,
                                     params=revision.id)

            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _('Revision already approved'))

    revision_form = QuestionSupervisorRevisionForm(instance=revision)
    tags = revision.tags.all()

    return render(request, '_questions/question_revision.html',
                  {'question': question, 'revision': revision, 'form': revision_form, 'tags': tags})


@login_required
def question_add_comment(request):
    question_id = request.POST['id']
    commnet_text = request.POST['comment']
    question = Question.objects.get(id=question_id)

    user = get_user(request)
    comment = QuestionComment()
    comment.user = user
    comment.text = commnet_text
    comment.question = question
    comment.save()

    if user.id == question.user_id:
        for question_comment in question.questioncomment_set.exclude(user=user):
            MessageUtil.send_message(user, question_comment.user, Message.TYPE_NEW_QUESTION_COMMENT, params=question.id)
    else:
        MessageUtil.send_message(user, question.user, Message.TYPE_NEW_QUESTION_COMMENT, params=question.id)

    return HttpResponse('')


@login_required
def question_scrap(request, question_id):
    user = get_user(request)
    question = Question.objects.get(id=question_id)
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    count = QuestionScrap.objects.filter(question_id=question_id, user=user).count()
    if count == 0:
        question.scrap += 1
        question.save()
        qscrap = QuestionScrap(question_id=question_id, user=user)
        qscrap.save()
        messages.add_message(request, messages.INFO, _('You have scrap this question.'))
    else:
        messages.add_message(request, messages.WARNING, _('You already scrap this question!'))
    return HttpResponseRedirect(url)


@login_required
def edit_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question = answer.question
    prev_revision = None

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
        if answer.answerrevision_set \
                .filter(status=AnswerRevision.STATUS_AWATING_APPROVAL).count() > 0:

            prev_revision = answer.answerrevision_set \
                                .filter(status=AnswerRevision.STATUS_AWATING_APPROVAL).order_by('-created')[:1][0]
            form = AnswerRevisionForm(instance=prev_revision)
            form.initial['editor_comment'] = ''
        else:
            form = AnswerRevisionForm(instance=answer_revision)

    return render(request, '_questions/answer_revision.html',
                  {'form': form, 'question': question, 'answer': answer, 'prev_revision': prev_revision})


@login_required
@permission_required(PERMISSION.AUTHORIZE_ANSWER_EDIT)
def authorize_answer_edit(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    supervisor = get_user(request)
    revision = answer.answerrevision_set.filter(status=AnswerRevision.STATUS_AWATING_APPROVAL).exclude(
        editor=supervisor).order_by('created')[:1][0]

    if not revision:
        messages.add_message(request, messages.WARNING, _('Nothing to review!'))
        return HttpResponseRedirect(URLS.QUESTIONS)

    if request.method == 'POST':
        revision_id = request.POST['revision_id']
        if int(revision_id) == revision.id:
            url = reverse(URLS.QUESTIONS)
            if 'not-approve' in request.POST:
                revision.status = AnswerRevision.STATUS_REJECTED
                revision.supervisor = supervisor
                revision.editor_comment = request.POST['editor_comment']
                revision.save()
                MessageUtil.send_message(supervisor, revision.editor, Message.TYPE_ANSWER_EDIT_DENIED,
                                         params=revision.id)
                return HttpResponseRedirect(url)

            revision.status = AnswerRevision.STATUS_APPROVED
            revision.supervisor = supervisor
            answer.text = revision.text
            answer.save()
            revision.save()
            context_info = 'answer_id:' + str(answer.id) + ';' + 'revision_id:' + str(revision.id)
            system_user = AppUtil.get_system_user()
            AppUtil.process_transaction(user_from=system_user, user_to=supervisor,
                                        amount=MitTransaction.AMOUNT_APPROVE_ANSWER_EDIT,
                                        trans_type=MitTransaction.TYPE_APPROVE_ANSWER_EDIT,
                                        context_info=context_info)

            amount = 0
            sophistication = request.POST['sophistication']
            if sophistication == '1':
                amount = MitTransaction.AMOUNT_EDIT_ANSWER_SMALL
            elif sophistication == '2':
                amount = MitTransaction.AMOUNT_EDIT_ANSWER_MIDDLE
            elif sophistication == '3':
                amount = MitTransaction.AMOUNT_EDIT_ANSWER_FULL

            AppUtil.process_transaction(user_from=system_user, user_to=revision.editor,
                                        amount=amount,
                                        trans_type=MitTransaction.TYPE_EDIT_ANSWER,
                                        context_info=context_info)

            MessageUtil.send_message(supervisor, revision.editor, Message.TYPE_ANSWER_EDIT_AUTHORIZED,
                                     params=revision.id)

            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _('Revision already approved'))

    form = AnswerSupervisorRevisionForm(instance=revision)
    return render(request, '_questions/answer_revision.html',
                  {'question': answer.question, 'answer': answer, 'revision': revision, 'form': form})


@login_required
def answer_add_comment(request):
    answer_id = request.POST['id']
    commnet_text = request.POST['comment']
    answer = Answer.objects.get(id=answer_id)

    comment = AnswerComment()
    comment.user = get_user(request)
    comment.text = commnet_text
    comment.answer = answer
    comment.save()

    user = get_user(request)

    if user.id == answer.user_id:
        for answer_comment in answer.answercomment_set.exclude(user=user):
            MessageUtil.send_message(user, answer_comment.user, Message.TYPE_NEW_ANSWER_COMMENT, params=answer.id)
    else:
        MessageUtil.send_message(user, answer.user, Message.TYPE_NEW_ANSWER_COMMENT, params=answer.id)
    return HttpResponse('')


@login_required
def answer_scrap(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    question = answer.question
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    count = AnswerScrap.objects.filter(answer_id=answer_id, user=user).count()
    if count == 0:
        answer.scrap += 1
        answer.save()
        ascrap = AnswerScrap(answer_id=answer_id, user=user)
        ascrap.save()
        messages.add_message(request, messages.INFO, _('You have scrap answer.'))
    else:
        messages.add_message(request, messages.WARNING, _('You already scrap this answer!'))
    return HttpResponseRedirect(url)


@login_required
def question_comment_scrap(request, question_comment_id):
    user = get_user(request)
    comment = QuestionComment.objects.get(id=question_comment_id)
    question = comment.question
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    count = QuestionCommentScrap.objects.filter(question_comment_id=question_comment_id, user=user).count()
    if count == 0:
        comment.scrap += 1
        comment.save()
        qcscrap = QuestionCommentScrap(question_comment_id=question_comment_id, user=user)
        qcscrap.save()
        messages.add_message(request, messages.INFO, _('You have scrap comment.'))
    else:
        messages.add_message(request, messages.WARNING, _('You already scrap this comment!'))
    return HttpResponseRedirect(url)


@login_required
def answer_comment_scrap(request, answer_comment_id):
    user = get_user(request)
    comment = AnswerComment.objects.get(id=answer_comment_id)
    question = comment.answer.question
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
    count = AnswerCommentScrap.objects.filter(answer_comment_id=answer_comment_id, user=user).count()
    if count == 0:
        comment.scrap += 1
        comment.save()
        acscrap = AnswerCommentScrap(answer_comment_id=answer_comment_id, user=user)
        acscrap.save()
        messages.add_message(request, messages.INFO, _('You have scrap comment.'))
    else:
        messages.add_message(request, messages.WARNING, _('You already scrap this comment!'))
    return HttpResponseRedirect(url)


@login_required
def vote_up_question(request, question_id):
    user = get_user(request)
    question = Question.objects.get(id=question_id)
    user_already_voted = question.votequestion_set.filter(user=user).count() != 0
    count_of_vote_in_day = VoteQuestion.objects.filter(user=user,
                                                       created__gt=datetime.datetime.today() - datetime.timedelta(
                                                           days=1)).count()
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))

    if user.id == question.user_id:
        messages.add_message(request, messages.WARNING, _('You can not vote for your question!'))
        return HttpResponseRedirect(url)

    if user_already_voted:
        messages.add_message(request, messages.WARNING, _('You can not vote more than once!'))
        return HttpResponseRedirect(url)

    if count_of_vote_in_day >= MitTransaction.DAY_VOTE_LIMIT:
        messages.add_message(request, messages.WARNING, _(
            'You can not vote more than ' + str(MitTransaction.DAY_VOTE_LIMIT) + ' times in 24 hours'))
        return HttpResponseRedirect(url)

    vote = VoteQuestion()
    vote.user = user
    vote.up = True
    vote.question = question

    votequestion_set = question.votequestion_set.filter(
        Q(mits__lt=MitTransaction.MAX_AMOUNT_VOTE_QUESTION) & Q(up=True))
    for votequestion in votequestion_set:
        user_from = AppUtil.get_system_user()
        user_to = votequestion.user
        votequestion.mits += MitTransaction.AMOUNT_VOTE_QUESTION
        context_info = 'question_id:' + str(question.id) + ';' + 'vote_id:' + str(vote.id)
        AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                    amount=MitTransaction.AMOUNT_VOTE_QUESTION,
                                    trans_type=MitTransaction.TYPE_VOTE_QUESTION, context_info=context_info)
        votequestion.save()

    vote.save()
    question.votes += 1
    if question.paid is False and question.votes == MitTransaction.VOTE_COUNT_ADD_QUESTION:
        user_from = AppUtil.get_system_user()
        user_to = question.user
        question.paid = True
        context_info = 'question_id:' + str(question.id) + ';' + 'vote_id:' + str(vote.id)
        AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                    amount=MitTransaction.AMOUNT_ADD_QUESTION,
                                    trans_type=MitTransaction.TYPE_ADD_QUESTION, context_info=context_info)
    question.save()
    return HttpResponseRedirect(url)


@login_required
def vote_down_question(request, question_id):
    user = get_user(request)
    question = Question.objects.get(id=question_id)
    user_already_voted = question.votequestion_set.filter(user=user).count() != 0
    count_of_vote_in_day = VoteQuestion.objects.filter(user=user,
                                                       created__gt=datetime.datetime.today() - datetime.timedelta(
                                                           days=1)).count()
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))

    if user.id == question.user_id:
        messages.add_message(request, messages.WARNING, _('You can not vote for your question!'))
        return HttpResponseRedirect(url)

    if user_already_voted:
        messages.add_message(request, messages.WARNING, _('You can not vote more than once!'))
        return HttpResponseRedirect(url)

    if count_of_vote_in_day >= MitTransaction.DAY_VOTE_LIMIT:
        messages.add_message(request, messages.WARNING, _(
            'You can not vote more than ' + str(MitTransaction.DAY_VOTE_LIMIT) + ' times in 24 hours'))
        return HttpResponseRedirect(url)

    vote = VoteQuestion()
    vote.user = user
    vote.question = question
    vote.up = False
    vote.save()
    question.votes -= 1
    question.save()
    return HttpResponseRedirect(url)


@login_required
def vote_up_answer(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    question = answer.question
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))

    user_already_voted = answer.voteanswer_set.filter(user=user).count() != 0
    count_of_vote_in_day = VoteAnswer.objects.filter(user=user,
                                                     created__gt=datetime.datetime.today() - datetime.timedelta(
                                                         days=1)).count()

    if user.id == answer.user_id:
        messages.add_message(request, messages.WARNING, _('You can not vote for your answer!'))
        return HttpResponseRedirect(url)

    if user_already_voted:
        messages.add_message(request, messages.WARNING, _('You can not vote more than once!'))
        return HttpResponseRedirect(url)

    if count_of_vote_in_day >= MitTransaction.DAY_VOTE_LIMIT:
        messages.add_message(request, messages.WARNING, _(
            'You can not vote more than ' + str(MitTransaction.DAY_VOTE_LIMIT) + ' times in 24 hours'))
        return HttpResponseRedirect(url)

    vote = VoteAnswer()
    vote.user = user
    vote.answer = answer
    vote.up = True

    voteanser_set = answer.voteanswer_set.filter(
        Q(mits__lt=MitTransaction.MAX_AMOUNT_VOTE_ANSWER) & Q(up=True))
    for voteanswer in voteanser_set:
        user_from = AppUtil.get_system_user()
        user_to = voteanswer.user
        voteanswer.mits += MitTransaction.AMOUNT_VOTE_ANSWER
        context_info = 'answer_id:' + str(answer.id) + ';' + 'vote_id:' + str(vote.id)
        AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                    amount=MitTransaction.AMOUNT_VOTE_ANSWER,
                                    trans_type=MitTransaction.TYPE_VOTE_ANSWER, context_info=context_info)
        voteanswer.save()

    vote.save()
    answer.votes += 1
    if answer.paid is False and answer.votes == MitTransaction.VOTE_COUNT_ADD_ANSWR:
        user_from = AppUtil.get_system_user()
        user_to = answer.user
        answer.paid = True
        context_info = 'answer_id:' + str(answer.id) + ';' + 'vote_id:' + str(vote.id)
        AppUtil.process_transaction(user_from=user_from, user_to=user_to,
                                    amount=MitTransaction.AMOUNT_ADD_ANSWER,
                                    trans_type=MitTransaction.TYPE_ADD_ANSWER, context_info=context_info)
    answer.save()
    return HttpResponseRedirect(url)


@login_required
def vote_down_answer(request, answer_id):
    user = get_user(request)
    answer = Answer.objects.get(id=answer_id)
    question = answer.question
    url = reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))

    user_already_voted = answer.voteanswer_set.filter(user=user).count() != 0
    count_of_vote_in_day = VoteAnswer.objects.filter(user=user,
                                                     created__gt=datetime.datetime.today() - datetime.timedelta(
                                                         days=1)).count()

    if user.id == answer.user_id:
        messages.add_message(request, messages.WARNING, _('You can not vote for your answer!'))
        return HttpResponseRedirect(url)

    if user_already_voted:
        messages.add_message(request, messages.WARNING, _('You can not vote more than once!'))
        return HttpResponseRedirect(url)

    if count_of_vote_in_day >= MitTransaction.DAY_VOTE_LIMIT:
        messages.add_message(request, messages.WARNING, _(
            'You can not vote more than ' + str(MitTransaction.DAY_VOTE_LIMIT) + ' times in 24 hours'))
        return HttpResponseRedirect(url)

    vote = VoteAnswer()
    vote.user = user
    vote.answer = answer
    vote.up = False
    vote.save()
    answer.votes -= 1
    answer.save()
    return HttpResponseRedirect(url)


@login_required
@permission_required(PERMISSION.ADD_TAG)
def create_tag(request):
    if request.method == 'POST':
        tag_exits = Tag.objects.filter(title=request.POST['title'].strip()).count() > 0
        if not tag_exits:
            tag = Tag()
            tag.user = get_user(request)
            form = TagForm(request.POST, instance=tag)
            form.save()
        else:
            messages.add_message(request, messages.WARNING, _('Tag already exits!'))
        url = reverse(URLS.CREATE_TAG)
        return HttpResponseRedirect(url)
    else:
        form = TagForm()

    return render(request, '_questions/tag_form.html', {'form': form})


@login_required
def find_tags(request):
    search = request.POST['search']
    tags_alredy_added = filter(None, request.POST['tags'].split(';'))
    tags = Tag.objects.filter(title__contains=search).exclude(id__in=tags_alredy_added)[:10]
    response = ''
    for tag in tags:
        response += '<li onclick="addTag(' + str(tag.id) + ', \'' + tag.title + '\')">' + tag.title + '</li>'
    return HttpResponse(response)


@user_passes_test(lambda u: u.groups.filter(name=PERMISSION_GROUPS.SUPERVISOR).exists())
def administration(request):
    return render(request, '_questions/administration.html')
