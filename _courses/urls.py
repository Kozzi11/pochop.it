from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required
from _courses.views import CourseDatatablesView, LessonDatatablesView, SlideDatatablesView, ComponentsDatatablesView

COURSES = 'courses'
COURSES_ALL = 'courses_all'
COURSES_IN_PROGRESS = 'courses_in-progress'
COURSES_COMPLETED = 'courses_completed'
COURSES_MY = 'courses_my'
COURSES_DATA = 'courses_data'
COURSES_GRID = 'courses_grid'
COURSE_NEW = 'course_new'
COURSE_EDIT = 'course_edit'
COURSE_MAIN = 'course_main'
COURSE_LESSONS = 'course_lessons'
COURSE_DELETE = 'course_delete'
COURSE_DESCRIPTION = 'course_description'
COURSE_ENROL = 'course_enrol'
COURSE_OPEN = 'course_open'

LESSONS_DATA = 'lessons_data'
LESSON_NEW = 'lesson_new'
LESSON_EDIT = 'lesson_edit'
LESSON_MAIN = 'lesson_main'
LESSON_DELETE = 'lesson_delete'

SLIDES_DATA = 'slides_data'
SLIDE_NEW = 'slide_new'
SLIDE_MAIN = 'slide_main'
SLIDE_DELETE = 'slide_delete'
SLIDE_EDIT_CONTENT = 'slide_edit_content'

COMPONENTS_DATA = 'components_data'
COMPONENT_NEW = 'component_new'
COMPONENT_SETTINGS = 'component_settings'
COMPONENT_DELETE = 'component_delete'
COMPONENT_CHANGE_ORDER = 'component_change_order'

urlpatterns = [

    url(r'^courses/$', login_required(views.courses), name=COURSES),
    url(r'^courses/all$', login_required(views.all_courses), name=COURSES_ALL),
    url(r'^courses/in_progress$', login_required(views.in_progress_courses), name=COURSES_IN_PROGRESS),
    url(r'^courses/completed$', views.completed_courses, name=COURSES_COMPLETED),
    url(r'^courses/my$', views.my_courses, name=COURSES_MY),
    url(r'^courses/data$', CourseDatatablesView.as_view(), name=COURSES_DATA),
    url(r'^courses/grid', views.grid_courses, name=COURSES_GRID),
    url(r'^course/new$', views.new_course, name=COURSE_NEW),
    url(r'^course/(.*)/edit$', views.edit_course, name=COURSE_EDIT),
    url(r'^course/(.*)/main_tab$', views.course_main_tab, name=COURSE_MAIN),
    url(r'^course/(.*)/lesssons_tab$', views.course_lessons_tab, name=COURSE_LESSONS),
    url(r'^course/(.*)/delete$', views.delete_course, name=COURSE_DELETE),
    url(r'^course/(.*)/description', views.course_description, name=COURSE_DESCRIPTION),
    url(r'^course/(.*)/enrol', views.course_enrol, name=COURSE_ENROL),
    url(r'^course/(.*)/open', views.course_open, name=COURSE_OPEN),

    url(r'^lessons/(.*)/data$', LessonDatatablesView.as_view(), name=LESSONS_DATA),
    url(r'^lesson/(.*)/new$', views.new_lesson, name=LESSON_NEW),
    url(r'^lesson/(.*)/edit$', views.edit_lesson, name=LESSON_EDIT),
    url(r'^lesson/(.*)/main_tab$', views.lesson_main_tab, name=LESSON_MAIN),
    url(r'^lesson/(.*)/delete$', views.delete_lesson, name=LESSON_DELETE),

    url(r'^slides/(.*)/data$', SlideDatatablesView.as_view(), name=SLIDES_DATA),
    url(r'^slide/(.*)/new$', views.new_slide, name=SLIDE_NEW),
    url(r'^slide/(.*)/main_tab$', views.slide_main_tab, name=SLIDE_MAIN),
    url(r'^slide/(.*)/delete$', views.delete_slide, name=SLIDE_DELETE),
    url(r'^slide/(.*)/edit/content$', views.edit_slide_content, name=SLIDE_EDIT_CONTENT),

    url(r'^components/(.*)/data$', ComponentsDatatablesView.as_view(), name=COMPONENTS_DATA),
    url(r'^component/(.*)/new$', views.new_component, name=COMPONENT_NEW),
    url(r'^component/(.*)/settings_tab$', views.component_settings_tab, name=COMPONENT_SETTINGS),
    url(r'^component/(.*)/delete$', views.delete_component, name=COMPONENT_DELETE),
    url(r'^component/(.*)/change_order$', views.component_change_order, name=COMPONENT_CHANGE_ORDER),

]
