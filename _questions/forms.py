from django import forms
from tinymce.widgets import TinyMCE
from _questions.models import Question, Tag, Answer


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}), required=False)
    tags = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = [
            'title',
            'text',
        ]


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}), required=False)

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
