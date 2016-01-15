from django import forms
from tinymce.widgets import TinyMCE
from _questions.models import Question, Tag, Answer
from django.utils.translation import ugettext as _


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}),
                           label=_("Concise description of the problem"), required=False)

    tags = forms.CharField(required=False, label=_("Tags"))

    class Meta:
        model = Question
        fields = [
            'title',
            'text',
        ]
        labels = {
            'title': _("Question heading")
        }


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}), required=False,
                           label=_("Your answer"))

    class Meta:
        model = Answer
        fields = [
            'text',
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'title',
            'description',
        ]
