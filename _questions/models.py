from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=254)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class QuestionComment(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    user = models.ForeignKey(User)
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=254)
    description = models.TextField()


class VoteQuestion(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    up = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)


class VoteAnswer(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    up = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

