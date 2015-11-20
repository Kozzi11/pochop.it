from django.conf.urls import url

from . import views
from _courses.views import CourseDatatablesView

urlpatterns = [
    url(r'^courses/data', CourseDatatablesView.as_view(),  name='course_datatables_view'),
    url(r'^courses/new$', views.new, name='courses_new'),
    url(r'^courses/edit-main/(.*)$', views.edit_main_tab, name='courses_edit_main'),
    url(r'^courses/edit-lesssons/(.*)$', views.edit_lessons_tab, name='courses_edit_lessons'),
    url(r'^courses/edit/(.*)', views.edit, name='courses_edit'),
    url(r'^courses/all$', views.all_tab, name='courses_all'),
    url(r'^courses/in_progress$', views.in_progress_tab, name='courses_in-progress'),
    url(r'^courses/completed$', views.completed_tab, name='courses_completed'),
    url(r'^courses/my$', views.my_tab, name='courses_my'),
    url(r'^courses/(.*)$', views.courses, name='courses'),
    url(r'^courses', views.courses, name='courses'),
]
