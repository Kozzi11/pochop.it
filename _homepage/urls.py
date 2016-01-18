from django.conf.urls import url

from . import views
from _homepage.constants import URLS

urlpatterns = [
    url(r'^$', views.homepage, name=URLS.HOMEPAGE),
    url(r'^about$', views.about, name=URLS.ABOUT),
]
