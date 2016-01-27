import bleach
from django import forms
from tinymce.widgets import TinyMCE
from _questions.models import Question, Tag, Answer, QuestionRevision, AnswerRevision
from django.utils.translation import ugettext as _
from pochopit import constants


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}),
                           label=_("Concise description of the problem"), required=True)

    tags = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={"placeholder": _("Tags")}))
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": _("Question heading")}))

    def clean_title(self):
        text = self.cleaned_data['title']
        return bleach.clean(text, tags=[], strip=True)

    def clean_text(self):
        text = self.cleaned_data['text']
        return bleach.clean(text, tags=constants.ALLOWED_TAGS)

    class Meta:
        model = Question
        fields = [
            'title',
            'text',
        ]


class QuestionRevisionForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}),
                           label='', required=True)

    tags = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={"placeholder": _("Tags")}))
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": _("Question heading")}))
    editor_comment = forms.CharField(label='',
                                     widget=forms.Textarea(attrs={'rows': 4, "placeholder": _("Editor comment")}))

    def clean_title(self):
        text = self.cleaned_data['title']
        return bleach.clean(text, tags=[], strip=True)

    def clean_text(self):
        text = self.cleaned_data['text']
        return bleach.clean(text, tags=constants.ALLOWED_TAGS)

    def clean_editor_comment(self):
        text = self.cleaned_data['editor_comment']
        return bleach.clean(text, tags=[])

    class Meta:
        model = QuestionRevision
        fields = [
            'title',
            'text',
            'tags',
            'editor_comment',
        ]


class QuestionSupervisorRevisionForm(QuestionRevisionForm):
    CHOICES = (
        ('1', _('low')),
        ('2', _('middle')),
        ('3', _('high')),
    )
    sophistication = forms.CharField(widget=forms.Select(choices=CHOICES), label=_('sophistication'))
    supervisor_comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False,
                                         label=_('Supervisor comment'))

    def __init__(self, *args, **kwargs):
        super(QuestionSupervisorRevisionForm, self).__init__(*args, **kwargs)
        del self.fields['editor_comment']


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}), required=True,
                           label=_("Your answer"))

    def clean_text(self):
        text = self.cleaned_data['text']
        return bleach.clean(text, tags=constants.ALLOWED_TAGS)

    class Meta:
        model = Answer
        fields = [
            'text',
        ]


class AnswerRevisionForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'rows': 15}),
                           label='', required=True)

    editor_comment = forms.CharField(label='',
                                     widget=forms.Textarea(attrs={'rows': 4, "placeholder": _("Editor comment")}))

    def clean_text(self):
        text = self.cleaned_data['text']
        return bleach.clean(text, tags=constants.ALLOWED_TAGS)

    def clean_editor_comment(self):
        text = self.cleaned_data['editor_comment']
        return bleach.clean(text, tags=[])

    class Meta:
        model = AnswerRevision
        fields = [
            'text',
            'editor_comment',
        ]


class AnswerSupervisorRevisionForm(AnswerRevisionForm):
    CHOICES = (
        ('1', _('low')),
        ('2', _('middle')),
        ('3', _('high')),
    )
    sophistication = forms.CharField(widget=forms.Select(choices=CHOICES), label=_('sophistication'))
    supervisor_comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False,
                                         label=_('Supervisor comment'))

    def __init__(self, *args, **kwargs):
        super(AnswerSupervisorRevisionForm, self).__init__(*args, **kwargs)
        del self.fields['editor_comment']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'title',
            'description',
        ]
