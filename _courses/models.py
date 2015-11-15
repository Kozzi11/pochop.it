from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)


class Lesson(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=30)
    order = models.IntegerField()


class Slide(models.Model):
    lesson = models.ForeignKey(Lesson)
    order = models.IntegerField()


class Component(models.Model):
    TYPES = (
        (1, 'Text'),
        (1, 'Image'),
    )
    parent = models.ForeignKey('self')
    type = models.IntegerField(choices=TYPES)
    order = models.IntegerField()


class CompoenentConfig(models.Model):
    component = models.ForeignKey(Component)
    key = models.IntegerField()
    value = models.CharField(max_length=254)
