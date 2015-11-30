from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from _courses.forms import CourseForm, LessonForm, SlideForm, ComponentForm
from _courses.models import Course, Lesson, Slide, ComponentData
from eztables.views import DatatablesView
from pochopit.viewcomponents.context_bar_item import ContextBarItem
from pochopit.viewcomponents.tab import Tab
from pochopit.viewcomponents.tab_group import TabGroup
from pochopit.viewcomponents.tabs_manager import TabsManager


def courses(request):
    tabs_manager = TabsManager(request, 'courses_all')
    tabs_manager.add_tab(
        Tab(_('All'), reverse('courses_all'), 'courses_all', is_active=True)
    )
    tabs_manager.add_tab(
        Tab(_('In progress'),  reverse('courses_in-progress'), 'courses_in-progress', buddge_number=2)
    )
    tabs_manager.add_tab(
        Tab(_('Completed'), reverse('courses_completed'), 'courses_completed', buddge_number=8)
    )
    tabs_manager.add_tab(
        Tab(_('My courses'), reverse('courses_my'), 'courses_my', buddge_number=3)
    )

    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs_manager.get_tabs()})


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
    course.title = _('Unnamed course')
    course.save()

    lesson = Lesson()
    lesson.title = _('Lesson 1')
    lesson.course = course
    lesson.order = 0
    lesson.save()

    slide = Slide()
    slide.lesson = lesson
    slide.title = _('Slide 1')
    slide.order = 0
    slide.save()

    component_data = ComponentData()
    component_data.title = _('Unnamed component')
    component_data.slide = slide
    component_data.type = ComponentData.TYPE_HTML
    component_data.order = 0
    component_data.save()

    url = "%s#course_main" % reverse('course_edit', args=(course.id,))
    return HttpResponseRedirect(url)


def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    url = "%s#courses_my" % reverse('courses')
    return HttpResponseRedirect(url)


def edit_course(request, course_id):

    tabs_manager = TabsManager(request, 'course_main')
    course = Course.objects.get(id=course_id)

    js_after_ajax = 'location.reload();'

    courses_tab_group = TabGroup(course.title)
    courses_tab_group.add_action_button(reverse('course_main', args=(course.id,)), 'pencil', short_name='course_main')
    courses_tab_group.add_action_button(reverse('lesson_new', args=(course.id,)), 'plus', js_after=js_after_ajax)

    for lesson in course.lesson_set.all():
        lessons_tab_group = TabGroup(lesson.title)
        lessons_tab_group.add_action_button(reverse('lesson_main', args=(lesson.id,)), 'pencil',
                                            short_name='lesson_main')
        lessons_tab_group.add_action_button(reverse('slide_new', args=(lesson.id,)), 'plus', js_after=js_after_ajax)
        for slide in lesson.slide_set.all():
            lessons_tab_group.add_tab(Tab(slide.title, reverse('course_main', args=(course_id,)), 'course_main'))
        courses_tab_group.add_tab_group(lessons_tab_group)

    tabs_manager.add_tab_group(courses_tab_group)

    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.title, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs_manager.get_tabs(),
                                                             'context_bar_items': context_bar_items})


def course_main_tab(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        form.save()
        return HttpResponseRedirect(reverse('course_edit', args=(course_id,)))
    else:
        form = CourseForm(instance=course)

    return render(request, '_courses/course/main.html', {'form': form, 'course_id': course_id})


def course_lessons_tab(request, course_id):
    return render(request, '_courses/course/lessons.html', {'course_id': course_id})


def new_lesson(request, course_id):
    course = Course.objects.get(id=course_id)
    lesson = Lesson()
    lesson.title = _('Unnamed lesson')
    lesson.course = course
    lesson.order = course.lesson_set.count()
    lesson.save()

    slide = Slide()
    slide.lesson = lesson
    slide.title = _('1. slide')
    slide.order = 0
    slide.save()

    component_data = ComponentData()
    component_data.title = _('Unnamed component')
    component_data.slide = slide
    component_data.type = ComponentData.TYPE_HTML
    component_data.order = 0
    component_data.save()

    return HttpResponse()


def edit_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course
    tabs = [
        Tab(_('Main'), reverse('lesson_main', args=(lesson_id,)), 'lesson_main'),
        Tab(_('Slides'), reverse('lesson_slides', args=(lesson_id,)), 'lesson_slides', is_active=True),
    ]
    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.title, reverse('lesson_main', args=(course.id,))),
        ContextBarItem(lesson.title, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs,
                                                             'context_bar_items': context_bar_items})


def lesson_main_tab(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        form.save()
        return HttpResponseRedirect(reverse('course_edit', args=(lesson.course.id,)))
    else:
        form = LessonForm(instance=lesson)

    return render(request, '_courses/lesson/main.html', {'form': form, 'lesson_id': lesson_id})


def lesson_slides_tab(request, lesson_id):
    return render(request, '_courses/lesson/slides.html', {'lesson_id': lesson_id})


def new_slide(request, lesson_id):
    slide = Slide()
    slide.lesson_id = lesson_id
    slide.order = 0
    slide.save()
    return HttpResponseRedirect(reverse('slide_edit', args=(slide.id,)))


def edit_slide(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    lesson = slide.lesson
    course = lesson.course
    tabs = [
        Tab(_('Main'), reverse('slide_main', args=(slide_id,)), 'slide_main'),
        Tab(_('Compenents'), reverse('slide_components', args=(slide_id,)), 'slide_components', is_active=True),
    ]
    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.title, reverse('course_edit', args=(course.id,))),
        ContextBarItem(lesson.title, reverse('lesson_edit', args=(lesson.id,))),
        ContextBarItem(slide.title, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs,
                                                             'context_bar_items': context_bar_items})


def slide_main_tab(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    if request.method == 'POST':
        form = SlideForm(request.POST, instance=slide)
        form.save()
        return HttpResponseRedirect(reverse('slide_edit', args=(slide_id,)))
    else:
        form = SlideForm(instance=slide)

    return render(request, '_courses/slide/main.html', {'form': form, 'slide_id': slide_id})


def slide_components_tab(request, slide_id):
    return render(request, '_courses/slide/components.html', {'slide_id': slide_id})


def new_component(request, slide_id):
    component = ComponentData()
    component.slide_id = slide_id
    component.type = 1
    component.order = 0
    component.save()
    return HttpResponseRedirect(reverse('component_edit', args=(component.id,)))


def edit_component(request, component_id):
    component = ComponentData.objects.get(id=component_id)
    slide = component.slide
    lesson = slide.lesson
    course = lesson.course
    tabs = [
        Tab(_('Main'), reverse('component_main', args=(component_id,)), 'component_main'),
        Tab(_('Settings'), reverse('component_settings', args=(component_id,)), 'component_settings', is_active=True),
    ]
    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.title, reverse('course_edit', args=(course.id,))),
        ContextBarItem(lesson.title, reverse('lesson_edit', args=(lesson.id,))),
        ContextBarItem(slide.title, reverse('slide_edit', args=(slide.id,))),
        ContextBarItem(component.title, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs,
                                                             'context_bar_items': context_bar_items})


def component_main_tab(request, component_id):
    component = ComponentData.objects.get(id=component_id)
    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component)
        form.save()
        return HttpResponseRedirect(reverse('component_edit', args=(component.id,)))
    else:
        form = ComponentForm(instance=component)

    return render(request, '_courses/component/main.html', {'form': form, 'component_id': component_id})


def component_settings_tab(request, component_id):
    return render(request, '_courses/component/settings.html', {'component_id': component_id})


class CourseDatatablesView(DatatablesView):
    model = Course
    fields = (
        'author__username',
        '{title}',
        'description',
        'id',
    )

    def post(self, request, *args, **kwargs):
        user = request.user
        self.queryset = Course.objects.filter(author=user)
        return super(CourseDatatablesView, self).post(request, args, kwargs)


class LessonDatatablesView(DatatablesView):
    model = Lesson
    fields = (
        'title',
        'id',
    )

    def post(self, request, *args, **kwargs):
        self.queryset = Lesson.objects.filter(course=args[0])
        return super(LessonDatatablesView, self).post(request, args, kwargs)


class SlideDatatablesView(DatatablesView):
    model = Slide
    fields = (
        'title',
        'id',
    )

    def post(self, request, *args, **kwargs):
        self.queryset = Slide.objects.filter(lesson=args[0])
        return super(SlideDatatablesView, self).post(request, args, kwargs)


class ComponentsDatatablesView(DatatablesView):
    model = ComponentData
    fields = (
        'title',
        'id',
    )

    def post(self, request, *args, **kwargs):
        self.queryset = ComponentData.objects.filter(slide=args[0])
        return super(ComponentsDatatablesView, self).post(request, args, kwargs)
