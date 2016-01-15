from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    STATUS_UNSEEN = 0

    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sender')
    text = models.TextField()
    notif_text = models.TextField()
    on_click_params = models.CharField(max_length=254)
    content_provider = models.IntegerField()
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
