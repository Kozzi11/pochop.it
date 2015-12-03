from django.conf.urls import url

from . import views

COMPONENT_HTML = 'component_html'

urlpatterns = [
    url(r'^component/html/(.*)$', views.html, name='component_html'),
]
