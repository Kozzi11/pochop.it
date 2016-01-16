from django.conf.urls import url

from . import views
from _messages.constants import URLS

urlpatterns = [
    url(r'^messages/notif$', views.get_notification_list, name=URLS.NOTIFICATION_LIST),
]
