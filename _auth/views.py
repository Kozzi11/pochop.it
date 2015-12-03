from django.http import HttpResponseRedirect
from django.shortcuts import render
from _auth.forms import SignUpForm
from django.contrib.auth.models import User


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('_auth/thanks.html')
    else:
        form = SignUpForm()
        return render(request, '_auth/sign_up.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return HttpResponseRedirect('/sing_up/success')
        else:
            form = SignUpForm()
            return render('_auth{sing_up.html', {'form': form})


