from django.forms import ModelForm
from _courses.models import Course, Lesson


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = [
            'name',
            'description'
        ]


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'name',
        ]
