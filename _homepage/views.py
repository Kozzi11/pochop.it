from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, '_homepage/homepage.html')


def about(request):
    return render(request, '_homepage/about.html')


def resticted_acces(request):
    return HttpResponse("Jen pro přihlášené")
