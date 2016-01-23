from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from _questions.constants import URLS
from _questions.models import Question, Answer, QuestionRevision, AnswerRevision


class Message(models.Model):
    STATUS_UNSEEN = 0
    STATUS_SEEN = 1
    STATUS_READ = 2
    STATUS_DELETED = 3

    TYPE_NEW_ANSWER = 0
    TYPE_NEW_QUESTION_COMMENT = 1
    TYPE_NEW_ANSWER_COMMENT = 2
    TYPE_QUESTION_EDIT_AUTHORIZED = 3
    TYPE_QUESTION_EDIT_DENIED = 4
    TYPE_ANSWER_EDIT_AUTHORIZED = 5
    TYPE_ANSWER_EDIT_DENIED = 6

    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sender')
    text = models.TextField()
    params = models.CharField(max_length=254)
    type = models.IntegerField()
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def get_notification_text(self):
        text = ''
        if self.type == self.TYPE_NEW_ANSWER:
            question_id = self.params
            question = Question.objects.get(id=question_id)
            text = '<span style="font-weight:bold">Nová odpověď na tvůj dotaz:</span><br>' + question.title

        elif self.type == self.TYPE_NEW_QUESTION_COMMENT:
            question_id = self.params
            question = Question.objects.get(id=question_id)
            text = '<span style="font-weight:bold">Nový komentář k tvému dotazu:</span><br>' + question.title

        elif self.type == self.TYPE_NEW_ANSWER_COMMENT:
            answer_id = self.params
            answer = Answer.objects.get(id=answer_id)
            text = '<span style="font-weight:bold">Nový komentář ke tvé odpovědi k otázce:</span><br>' + \
                   answer.question.title

        elif self.type == self.TYPE_QUESTION_EDIT_AUTHORIZED:
            revision_id = self.params
            revision = QuestionRevision.objects.get(id=revision_id)
            text = '<span style="font-weight:bold">Schváleny úpravy otázky:</span><br>' + revision.question.title

        elif self.type == self.TYPE_ANSWER_EDIT_AUTHORIZED:
            revision_id = self.params
            revision = AnswerRevision.objects.get(id=revision_id)
            text = '<span style="font-weight:bold">Schváleny úpravy odpovědi u otázky:</span><br>' + \
                   revision.answer.question.title

        elif self.type == self.TYPE_QUESTION_EDIT_DENIED:
            revision_id = self.params
            revision = QuestionRevision.objects.get(id=revision_id)
            text = '<span style="font-weight:bold">Zamítnuty úpravy otázky:</span><br>' + revision.question.title

        elif self.type == self.TYPE_ANSWER_EDIT_DENIED:
            revision_id = self.params
            revision = AnswerRevision.objects.get(id=revision_id)
            text = '<span style="font-weight:bold">Zamítnuty úpravy odpovědi u otázky:</span><br>' + \
                   revision.answer.question.title

        return text

    def get_url(self):
        question_id = self.params
        question = Question.objects.get(id=question_id)
        return reverse(URLS.VIEW_QUESTION, args=(question.id, question.title.replace(' ', '-')))
