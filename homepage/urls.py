from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kokos$', views.resticted_acces, name='resticted_acces'),
]
