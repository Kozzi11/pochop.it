from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from _courses.models import Course
from eztables.views import DatatablesView
from pochopit.viewcomponents.tab import Tab


def courses(request):
    tabs = [
            Tab(_('All'), reverse('courses_all'), True),
            Tab(_('In progress'), reverse('courses_in_progress'), False, 2),
            Tab(_('Completed'), reverse('courses_completed'), False, 8),
            Tab(_('My courses'), reverse('courses_my'), False, 3)
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs})


def all_tab(request):
    return render(request, '_courses/all.html')


def in_progress_tab(request):
    return render(request, '_courses/in_progress.html')


def completed_tab(request):
    return render(request, '_courses/completed.html')


def my_tab(request):
    return render(request, '_courses/my.html')


def new(request):
    course = Course()
    course.author = get_user(request)
    course.save()
    return HttpResponseRedirect(reverse('courses_edit', args=(course.id,)))


def edit(request, course_id):
    tabs = [
        Tab(_('Main'), reverse('courses_edit_main_tab', args=(course_id,)), True),
        Tab(_('Lessons'), reverse('courses_edit_lessons_tab', args=(course_id,)), False),
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs})


def edit_main_tab(request, course_id):
    return render(request, '_courses/edit/main.html')


def edit_lessons_tab(request, course_id):
    return render(request, '_courses/edit/lessons.html')


class CourseDatatablesView(DatatablesView):
    model = Course
    fields = (
        'author',
        'name',
        'description',
    )
