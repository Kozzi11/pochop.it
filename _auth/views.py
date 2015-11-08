from django.http import HttpResponseRedirect
from django.shortcuts import render
from _auth.forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = SignUpForm()
        return render(request, '_auth/sign_up.html', {'form': form})
