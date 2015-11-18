from django.conf.urls import url

from . import views
from _courses.views import CourseDatatablesView

urlpatterns = [
    url(r'^courses/data', CourseDatatablesView.as_view(),  name='course_datatables_view'),
    url(r'^courses/new$', views.new, name='courses_new'),
    url(r'^courses/edit/(.*)$', views.edit, name='courses_edit'),
    url(r'^courses/edit-main-tab/(.*)$', views.edit_main_tab, name='courses_edit_main_tab'),
    url(r'^courses/edit-lessons-tab/(.*)$', views.edit_lessons_tab, name='courses_edit_lessons_tab'),
    url(r'^courses/all$', views.all_tab, name='courses_all'),
    url(r'^courses/in_progress$', views.in_progress_tab, name='courses_in_progress'),
    url(r'^courses/completed$', views.completed_tab, name='courses_completed'),
    url(r'^courses/my$', views.my_tab, name='courses_my'),
    url(r'^courses', views.courses, name='courses'),

]
