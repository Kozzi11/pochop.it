from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from _auth.forms import SignUpForm
from django.contrib.auth.models import User
from pochopit.models import UserSetting


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
            user_setting = UserSetting()
            user_setting.user = user
            user_setting.save()
            return HttpResponseRedirect('/sing_up/success')
        else:
            form = SignUpForm()
            return render(request, '_auth/sign_up.html', {'form': form})

    form = SignUpForm()
    return render(request, '_auth/sign_up.html', {'form': form})

