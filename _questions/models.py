from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=254)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    user = models.ForeignKey(User)
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=254)
    description = models.TextField()
