from django.forms import ModelForm
from _courses.models import Course, Lesson, Slide, Component


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
        ]


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'order',
        ]


class SlideForm(ModelForm):
    class Meta:
        model = Slide
        fields = [
            'title',
            'order',
        ]


class ComponentForm(ModelForm):
    class Meta:
        model = Component
        fields = [
            'title',
            'type',
            'order',
        ]

