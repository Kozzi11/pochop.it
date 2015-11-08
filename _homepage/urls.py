from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^kokos$', views.resticted_acces, name='_homepage.views.resticted_acces'),
]
