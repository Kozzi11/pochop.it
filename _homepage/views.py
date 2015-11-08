from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def homepage(request):
    _("test prekladu")
    return render(request, '_homepage/homepage.html')


@login_required
def resticted_acces(request):
    return HttpResponse("Jen pro přihlášené")
