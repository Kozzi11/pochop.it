from django.conf.urls import url

from . import views
from _courses.views import CourseDatatablesView, LessonDatatablesView

urlpatterns = [
    url(r'^lessons/data', LessonDatatablesView.as_view(),  name='course_lessons_datatables_view'),
    url(r'^courses/data', CourseDatatablesView.as_view(),  name='course_datatables_view'),
    url(r'^course/new', views.new_course, name='courses_new'),
    url(r'^lesson/(.*)/new', views.new_lesson, name='courses_lesson_new'),
    url(r'^courses/(.*)/edit-lesson-main', views.lesson_main_tab, name='courses_lesson_edit_main'),
    url(r'^courses/(.*)/edit-lesson-slides', views.lesson_slides_tab, name='courses_lesson_edit_slides'),
    url(r'^courses/(.*)/edit-main', views.course_main_tab, name='courses_edit_main'),
    url(r'^courses/(.*)/edit-lesssons', views.course_lessons_tab, name='courses_edit_lessons'),
    url(r'^courses/(.*)/edit-lesson', views.edit_lesson, name='courses_edit_lesson'),
    url(r'^courses/(.*)/edit', views.edit_course, name='courses_edit'),
    url(r'^courses/all', views.all_courses, name='courses_all'),
    url(r'^courses/in_progress', views.in_progress_courses, name='courses_in-progress'),
    url(r'^courses/completed', views.completed_courses, name='courses_completed'),
    url(r'^courses/my', views.my_courses, name='courses_my'),
    url(r'^courses', views.courses, name='courses'),
]
