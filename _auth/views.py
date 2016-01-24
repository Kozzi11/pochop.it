from django.contrib import auth
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from _auth.constants import URLS
from _auth.forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User
from _questions.models import Question, Answer, VoteQuestion, VoteAnswer, QuestionRevision, AnswerRevision
from pochopit.models import UserProfile, MitTransaction


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'])
            user = auth.authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            auth.login(request, user)
            user_setting = UserProfile()
            user_setting.user = user
            user_setting.save()
            return HttpResponseRedirect('/sing_up/success')
        else:
            form = SignUpForm()
            return render(request, '_auth/sign_up.html', {'form': form})

    form = SignUpForm()
    return render(request, '_auth/sign_up.html', {'form': form})


@login_required
def profile(request, user_id):
    profile_user = User.objects.get(id=user_id)
    stats = get_stats(profile_user)
    return render(request, '_auth/profile.html', {'stats': stats,'profile_user': profile_user})


@login_required
def my_profile(request):
    user = get_user(request)
    stats = get_stats(user)
    profile_user = user
    return render(request, '_auth/profile.html', {'stats': stats, 'profile_user': profile_user})


@login_required
def my_profile_edit(request):
    user = get_user(request)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            profile = user.userprofile
            profile.businesscard = form.cleaned_data['businesscard']
            profile.save()
            user.save()
            url = reverse(URLS.MY_PROFILE)
            return HttpResponseRedirect(url)
    else:
        form = ProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                                    'businesscard': user.userprofile.businesscard})

    return render(request, '_auth/profile_edit.html', {'form': form})


def get_stats(user):
    questions_stats = {'mits': 0,
                       'count': Question.objects.filter(user=user).count()}

    answers_stats = {'mits': 0,
                     'count': Answer.objects.filter(user=user).count()}

    edits_stats = {'mits': 0,
                   'count': QuestionRevision.objects.filter(editor=user).count() + AnswerRevision.objects.filter(
                       editor=user).count()}

    votes_stats = {'mits': 0,
                   'count': VoteQuestion.objects.filter(user=user).count() + VoteAnswer.objects.filter(
                       user=user).count()}

    admin_stats = {'mits': 0, 'count': 0}

    summary = {'mits': 0, 'count': 0}

    types = (
        MitTransaction.TYPE_ADD_QUESTION,
        MitTransaction.TYPE_ADD_ANSWER,
        MitTransaction.TYPE_EDIT_QUESTION,
        MitTransaction.TYPE_EDIT_ANSWER,
        MitTransaction.TYPE_VOTE_QUESTION,
        MitTransaction.TYPE_VOTE_ANSWER,
        MitTransaction.TYPE_APPROVE_QUESTION_EDIT,
        MitTransaction.TYPE_APPROVE_ANSWER_EDIT,
    )
    query_set = MitTransaction.objects.filter(user_to=user, type__in=types)
    for transaction in query_set:
        if transaction.type == MitTransaction.TYPE_ADD_QUESTION:
            questions_stats['mits'] += transaction.amount
        elif transaction.type == MitTransaction.TYPE_ADD_ANSWER:
            answers_stats['mits'] += transaction.amount
        elif transaction.type == MitTransaction.TYPE_EDIT_QUESTION or MitTransaction.TYPE_EDIT_ANSWER:
            edits_stats['mits'] += transaction.amount
        elif transaction.type == MitTransaction.TYPE_VOTE_QUESTION or MitTransaction.TYPE_VOTE_ANSWER:
            votes_stats['mits'] += transaction.amount
        else:
            admin_stats['mits'] += transaction.amount
            admin_stats['count'] += 1

    summary['count'] = questions_stats['count'] + answers_stats['count'] + edits_stats['count'] + votes_stats[
        'count'] + admin_stats['count']

    summary['mits'] = questions_stats['mits'] + answers_stats['mits'] + edits_stats['mits'] + votes_stats[
        'mits'] + admin_stats['mits']

    poradit = {
        'questions': questions_stats,
        'answers': answers_stats,
        'edits': edits_stats,
        'votes': votes_stats,
        'admin': admin_stats,
        'summary': summary,
    }
    stats = {'poradit': poradit}
    return stats
