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
    scrap = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    status = models.IntegerField(default=STATUS_ACTIVE)
    created = models.DateTimeField(auto_now_add=True)

    def has_active_revision(self, user):
        return self.questionrevision_set.filter(status=QuestionRevision.STATUS_AWATING_APPROVAL).exclude(
            editor=user).count() > 0


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
    sophistication = models.IntegerField(default=0)
    status = models.IntegerField(default=STATUS_AWATING_APPROVAL)
    created = models.DateTimeField(auto_now_add=True)


class QuestionComment(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField()
    scrap = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class QuestionScrap(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


class QuestionCommentScrap(models.Model):
    question_comment = models.ForeignKey(QuestionComment)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    text = models.TextField()
    votes = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    scrap = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def has_active_revision(self, user):
        return self.answerrevision_set.filter(status=AnswerRevision.STATUS_AWATING_APPROVAL).exclude(
            editor=user).count() > 0


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
    sophistication = models.IntegerField(default=0)
    status = models.IntegerField(default=STATUS_AWATING_APPROVAL)
    created = models.DateTimeField(auto_now_add=True)


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    text = models.TextField()
    scrap = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class AnswerScrap(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)


class AnswerCommentScrap(models.Model):
    answer_comment = models.ForeignKey(AnswerComment)
    user = models.ForeignKey(User)
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
    mits = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


class VoteAnswer(models.Model):
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)
    up = models.BooleanField()
    mits = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
