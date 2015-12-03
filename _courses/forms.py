from django import forms
from tinymce.widgets import TinyMCE
from _courses.models import Course, Lesson, Slide, ComponentData


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
        ]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'order',
        ]


class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = [
            'title',
            'order',
        ]


class ComponentForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'rows': 25}), required=False)

    class Meta:
        model = ComponentData
        fields = [
            'title',
            'type',
            'order',
        ]
