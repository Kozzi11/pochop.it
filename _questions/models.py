from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    STATUS_ACTIVE = 0
    STATUS_DELETED = 1

    user = models.ForeignKey(User)
    title = models.CharField(max_length=254)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    status = models.IntegerField(default=STATUS_ACTIVE)
    created = models.DateTimeField(auto_now_add=True)

    def has_active_revision(self):
        return self.questionrevision_set.filter(status=QuestionRevision.STATUS_AWATING_APPROVAL).count() > 0


class QuestionRevision(models.Model):
    STATUS_AWATING_APPROVAL = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2

    question = models.ForeignKey(Question)
    editor = models.ForeignKey(User)
    supervisor = models.ForeignKey(User, default=0, related_name='supervisor')
    title = models.CharField(max_length=254)
    text = models.TextField()
    tags = models.ManyToManyField('Tag')
    editor_comment = models.TextField()
    supervisor_comment = models.TextField()
    status = models.IntegerField(default=STATUS_AWATING_APPROVAL)
    created = models.DateTimeField(auto_now_add=True)


class QuestionComment(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def has_active_revision(self):
        return self.answerrevision_set.filter(status=AnswerRevision.STATUS_AWATING_APPROVAL).count() > 0


class AnswerRevision(models.Model):
    STATUS_AWATING_APPROVAL = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2

    answer = models.ForeignKey(Answer)
    editor = models.ForeignKey(User)
    supervisor = models.ForeignKey(User, default=0, related_name='answer_rev_supervisor')
    text = models.TextField()
    editor_comment = models.TextField()
    supervisor_comment = models.TextField()
    status = models.IntegerField(default=STATUS_AWATING_APPROVAL)
    created = models.DateTimeField(auto_now_add=True)


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer)
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
