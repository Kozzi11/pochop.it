from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from _courses.models import Course
from eztables.views import DatatablesView
from pochopit.viewcomponents.tab import Tab


def courses(request, tab='#in-progress'):
    tabs = [
            Tab(_('All'), 'courses_all', is_active=True),
            Tab(_('In progress'), 'courses_in-progress', buddge_number=2),
            Tab(_('Completed'), 'courses_completed', buddge_number=8),
            Tab(_('My courses'), 'courses_my', buddge_number=3)
    ]

    active_tab = tabs[0]

    if tab == '#all':
        active_tab = tabs[0]

    if tab == '#in-progress':
        active_tab = tabs[1]

    if tab == '#completed':
        active_tab = tabs[2]

    if tab == '#my':
        active_tab = tabs[3]

    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs, 'active_tab': active_tab})


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


def edit(request, course_id, tab='#main'):
    tabs = [
        Tab(_('Main'), 'courses_edit_main', params=(course_id,), is_active=True),
        Tab(_('Lessons'), 'courses_edit_lessons', params=(course_id,)),
    ]

    active_tab = tabs[0]

    if tab == '#main':
        active_tab = tabs[0]

    if tab == '#lessons':
        active_tab = tabs[1]

    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs, 'active_tab': active_tab})


def edit_main_tab(request, course_id):
    return render(request, '_courses/edit/main.html')


def edit_lessons_tab(request, course_id):
    return render(request, '_courses/edit/lessons.html')


class CourseDatatablesView(DatatablesView):
    model = Course
    fields = (
        'author__username',
        '{name}',
        'description',
        'id',
    )
