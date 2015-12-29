from django import forms
from tinymce.widgets import TinyMCE
from _questions.models import Question, Tag


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}), required=False)
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = [
            'title',
            'text',
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'title',
            'description',
        ]