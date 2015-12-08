from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=254)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class UserCourse(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    completed = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=254)
    order = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class Slide(models.Model):
    lesson = models.ForeignKey(Lesson)
    title = models.CharField(max_length=254)
    order = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class ComponentData(models.Model):
    TYPE_HTML = 1
    TYPE_IMAGE = 2

    TYPES = {
        TYPE_HTML: 'HTML',
        TYPE_IMAGE: 'IMAGE',
    }

    # parent = models.ForeignKey('self')
    slide = models.ForeignKey(Slide)
    title = models.CharField(max_length=254)
    type = models.IntegerField(choices=TYPES.items())
    order = models.IntegerField()


class ComponentConfig(models.Model):

    KEY_CONTENT = 1

    componentData = models.ForeignKey(ComponentData)
    key = models.IntegerField()
    value = models.TextField()
