from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from _questions.constants import URLS
from _questions.models import Question


class Message(models.Model):
    STATUS_UNSEEN = 0
    STATUS_SEEN = 1
    STATUS_READ = 2

    TYPE_QUESTION = 0

    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sender')
    text = models.TextField()
    params = models.CharField(max_length=254)
    type = models.IntegerField()
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def get_notification_text(self):
        text = ''
        if self.type == self.TYPE_QUESTION:
            question_id = self.params
            question = Question.objects.get(id=question_id)
            text = '<span style="font-weight:bold">Nová reakce na tvůj dotaz:</span><br>' + question.title

        return text

    def get_url(self):
        question_id = self.params
        question = Question.objects.get(id=question_id)
        return reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
