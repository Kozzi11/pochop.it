from django.conf.urls import url

from . import views
from _homepage.constants import URLS

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about$', views.about, name=URLS.ABOUT),
    url(r'^kokos$', views.resticted_acces, name='_homepage.views.resticted_acces'),
]
