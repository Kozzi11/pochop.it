import bleach
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from pochopit import constants


class SignUpForm(forms.Form):
    username = forms.CharField(label=_('Username'), min_length=4, max_length=100)
    email = forms.EmailField(label=_('E-mail'),  max_length=254, required=True)
    password = forms.CharField(label=_('Password'), min_length=6, widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput, required=True)

    def clean_username(self):
        text = self.cleaned_data['username']
        return bleach.clean(text, tags=[])

    def clean_email(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(
            _("This email is already registered. If you've forgotten your password, generate a new one."))

    def clean_password_confirm(self):
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError(_("The two password fields did not match!"))
        return self.cleaned_data['password_confirm']


class LoginForm(AuthenticationForm):
        username = forms.CharField(max_length=254, label=_('E-mail'))


class ProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=100)
    last_name = forms.CharField(label=_('Last name'), max_length=100)
    email = forms.EmailField(label=_('E-mail'), max_length=254, required=True)
    businesscard = forms.CharField(widget=TinyMCE(attrs={'rows': 15}), required=False, label=_("Other info"))

    def clean_first_name(self):
        text = self.cleaned_data['first_name']
        return bleach.clean(text, tags=[])

    def clean_last_name(self):
        text = self.cleaned_data['last_name']
        return bleach.clean(text, tags=[])

    def clean_businesscard(self):
        text = self.cleaned_data['businesscard']
        return bleach.clean(text, tags=constants.ALLOWED_TAGS)
