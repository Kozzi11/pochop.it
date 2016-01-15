from django.conf.urls import url

from . import views

ABOUT = 'about'

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about$', views.about, name=ABOUT),
    url(r'^kokos$', views.resticted_acces, name='_homepage.views.resticted_acces'),
]
