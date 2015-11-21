from django.conf.urls import url

from . import views
from _courses.views import CourseDatatablesView, LessonDatatablesView, SlideDatatablesView, ComponentsDatatablesView

urlpatterns = [

    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/all$', views.all_courses, name='courses_all'),
    url(r'^courses/in_progress$', views.in_progress_courses, name='courses_in-progress'),
    url(r'^courses/completed$', views.completed_courses, name='courses_completed'),
    url(r'^courses/my$', views.my_courses, name='courses_my'),
    url(r'^courses/data$', CourseDatatablesView.as_view(),  name='courses_data'),
    url(r'^course/new$', views.new_course, name='course_new'),
    url(r'^course/(.*)/edit$', views.edit_course, name='course_edit'),
    url(r'^course/(.*)/main_tab$', views.course_main_tab, name='course_main'),
    url(r'^course/(.*)/lesssons_tab$', views.course_lessons_tab, name='course_lessons'),

    url(r'^lessons/(.*)/data$', LessonDatatablesView.as_view(),  name='lessons_data'),
    url(r'^lesson/(.*)/new$', views.new_lesson, name='lesson_new'),
    url(r'^lesson/(.*)/edit$', views.edit_lesson, name='lesson_edit'),
    url(r'^lesson/(.*)/main_tab$', views.lesson_main_tab, name='lesson_main'),
    url(r'^lesson/(.*)/slides_tab$', views.lesson_slides_tab, name='lesson_slides'),

    url(r'^slides/(.*)/data$', SlideDatatablesView.as_view(),  name='slides_data'),
    url(r'^slide/(.*)/new$', views.new_slide, name='slide_new'),
    url(r'^slide/(.*)/edit$', views.edit_slide, name='slide_edit'),
    url(r'^slide/(.*)/main_tab$', views.slide_main_tab, name='slide_main'),
    url(r'^slide/(.*)/components_tab$', views.slide_components_tab, name='slide_components'),

    url(r'^components/(.*)/data$', ComponentsDatatablesView.as_view(),  name='components_data'),
    url(r'^component/(.*)/new$', views.new_component, name='component_new'),
    url(r'^component/(.*)/edit$', views.edit_component, name='component_edit'),
    url(r'^component/(.*)/main_tab$', views.component_main_tab, name='component_main'),
    url(r'^component/(.*)/settings_tab$', views.component_settings_tab, name='component_settings'),

]
