from django.utils.translation import ugettext as _
from django import forms


class SignUpForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=100)
    last_name = forms.CharField(label=_('Last name'), max_length=100)
    age = forms.IntegerField(label=_('Age'))
