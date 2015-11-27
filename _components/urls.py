from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^component/html/(.*)$', views.html, name='component_html'),
]
