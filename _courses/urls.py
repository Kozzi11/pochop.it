from django.conf.urls import url

from . import views
from _courses.views import CourseDatatablesView

urlpatterns = [
    url(r'^courses/kokos$', CourseDatatablesView.as_view(),  name='course_datatables_view'),
    url(r'^courses/new$', views.new, name='courses_new'),
    url(r'^courses/edit/(.*)$', views.edit, name='courses_edit'),
    url(r'^courses/(.*)$', views.courses, name='courses'),
]
