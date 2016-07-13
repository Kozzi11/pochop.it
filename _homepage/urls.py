from django.conf.urls import url

from . import views
from _homepage.constants import URLS

urlpatterns = [
    url(r'^$', views.homepage, name=URLS.HOMEPAGE),
    url(r'^about$', views.about, name=URLS.ABOUT),
    url(r'^connect$', views.connect, name=URLS.CONNECT),
]
