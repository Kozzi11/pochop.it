from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from django_tables2 import RequestConfig
from _courses.models import Course
from _courses.tables import CourseTable
from eztables.views import DatatablesView
from pochopit.viewcomponents.tab import Tab


def courses(request, tab_name):
    if not tab_name:
        tab_name = 'in_progress'

    tabs = [
            Tab(_('All'), reverse('courses', args=('all',)), tab_name == 'all'),
            Tab(_('In progress'), reverse('courses', args=('in_progress',)), tab_name == 'in_progress', 2),
            Tab(_('Completed'), reverse('courses', args=('completed',)), tab_name == 'completed', 8),
            Tab(_('My courses'), reverse('courses', args=('my',)), tab_name == 'my', 3)
    ]

    template_name = '_courses/' + tab_name + '.html'

    table = CourseTable(Course.objects.all())
    RequestConfig(request).configure(table)
    return render(request, template_name, {'tabs': tabs, 'courses': table})


def new(request):
    course = Course()
    course.author = get_user(request)
    course.save()
    return HttpResponseRedirect(reverse('courses_edit', args=(course.id,)))


def edit(request, id):
    return HttpResponse("test")


class CourseDatatablesView(DatatablesView):
    model = Course
    fields = (
        'author',
        'name',
        'description',
    )
