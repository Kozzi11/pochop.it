from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from homepage.forms import NameForm
from django.contrib.auth.decorators import login_required


def index(request):
    _("test prekladu")
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
        return render(request, 'homepage/index.html', {'form': form})


@login_required
def resticted_acces(request):
    return HttpResponse("Jen pro přihlášené")
