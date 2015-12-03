from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    first_name = forms.CharField(label=_('First name'), max_length=100)
    last_name = forms.CharField(label=_('Last name'), max_length=100)
    age = forms.IntegerField(label=_('Age'))
    email = forms.EmailField(label=_('E-mail'), max_length=254, required=True)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput, required=True)

    def unique_user(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("This email is already registered. If you've forgotten your password, generate a new one."))

    def confirm_password(self):
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError(_("The two password fields did not match!"))
        return self.cleaned_data