from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from _courses.forms import CourseForm, LessonForm
from _courses.models import Course, Lesson
from eztables.views import DatatablesView
from pochopit.viewcomponents.context_bar_item import ContextBarItem
from pochopit.viewcomponents.tab import Tab


def courses(request):
    tabs = [
        Tab(_('All'), 'courses_all', is_active=True),
        Tab(_('In progress'), 'courses_in-progress', buddge_number=2),
        Tab(_('Completed'), 'courses_completed', buddge_number=8),
        Tab(_('My courses'), 'courses_my', buddge_number=3)
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs})


def all_courses(request):
    return render(request, '_courses/all.html')


def in_progress_courses(request):
    return render(request, '_courses/in_progress.html')


def completed_courses(request):
    return render(request, '_courses/completed.html')


def my_courses(request):
    return render(request, '_courses/my.html')


def new_course(request):
    course = Course()
    course.author = get_user(request)
    course.save()
    return HttpResponseRedirect(reverse('courses_edit', args=(course.id,)))


def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    tabs = [
        Tab(_('Main'), 'courses_edit_main', params=(course_id,)),
        Tab(_('Lessons'), 'courses_edit_lessons', params=(course_id,), is_active=True),
    ]
    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.name, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs,
                                                             'context_bar_items': context_bar_items})


def course_main_tab(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        form.save()
        return HttpResponseRedirect(reverse('courses_edit', args=(course_id,)))
    else:
        form = CourseForm(instance=course)

    return render(request, '_courses/edit/main.html', {'form': form, 'course_id': course_id})


def course_lessons_tab(request, course_id):
    return render(request, '_courses/edit/lessons.html', {'course_id': course_id})


def new_lesson(request, course_id):
    lesson = Lesson()
    lesson.name = _('undefined')
    lesson.course_id = course_id
    lesson.order = 0
    lesson.save()
    return HttpResponseRedirect(reverse('courses_edit_lesson', args=(lesson.id,)))


def edit_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course
    tabs = [
        Tab(_('Main'), 'courses_lesson_edit_main', params=(lesson_id,)),
        Tab(_('Slides'), 'courses_lesson_edit_slides', params=(lesson_id,), is_active=True),
    ]
    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.name, reverse('courses_edit', args=(course.id,))),
        ContextBarItem(lesson.name, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs,
                                                             'context_bar_items': context_bar_items})


def lesson_main_tab(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        form.save()
        return HttpResponseRedirect(reverse('courses_edit_lesson', args=(lesson_id,)))
    else:
        form = LessonForm(instance=lesson)

    return render(request, '_courses/lessons/main.html', {'form': form, 'lesson_id': lesson_id})


def lesson_slides_tab(request, lesson_id):
    return render(request, '_courses/lessons/slides.html', {'lesson_id': lesson_id})


class CourseDatatablesView(DatatablesView):
    model = Course
    fields = (
        'author__username',
        '{name}',
        'description',
        'id',
    )


class LessonDatatablesView(DatatablesView):
    model = Lesson
    fields = (
        'name',
        'id',
    )
