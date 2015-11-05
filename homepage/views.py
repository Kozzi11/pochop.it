from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.shortcuts import render
from homepage.forms import NameForm


def index(request):
    _("test prekladu")
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
        return render(request, 'homepage/index.html', {'form': form})
