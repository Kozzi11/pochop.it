from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required
from _messages.constants import URLS

urlpatterns = [
    url(r'^messages/notif$', login_required(views.get_notification_list), name=URLS.NOTIFICATION_LIST),
]
