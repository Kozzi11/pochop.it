from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from _courses.forms import CourseForm, LessonForm, SlideForm, ComponentForm
from _courses.models import Course, Lesson, Slide, ComponentData
from eztables.views import DatatablesView
from pochopit.viewcomponents.context_bar_item import ContextBarItem
from pochopit.viewcomponents.tab import Tab
from pochopit.viewcomponents.tab_group import TabGroup


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
    return HttpResponseRedirect(reverse('course_edit', args=(course.id,)))


def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    tabs = [
        # Tab(course.title, 'course_main', params=(course_id,)),
        # Tab(_('Lessons'), 'course_lessons', params=(course_id,), is_active=True),
    ]

    courses_tab_group = TabGroup(course.title)

    for lesson in course.lesson_set.all():
        lessons_tab_group = TabGroup(lesson.title)
        lessons_tab_group.add_action_button('slide_new', reverse('slide_new', args=(lesson.id,)), 'plus')
        lessons_tab_group.add_action_button('lesson_main', reverse('lesson_main', args=(lesson.id,)), 'pencil')
        for slide in lesson.slide_set.all():
            lessons_tab_group.add_tab(Tab(slide.title, 'course_main', params=(course_id,)))
        courses_tab_group.add_tab_group(lessons_tab_group)

    tabs += courses_tab_group.get_items()

    context_bar_items = [
        ContextBarItem(_('Courses'), reverse('courses')),
        ContextBarItem(course.title, '#')
    ]
    return render(request, 'pochopit/base_side_panel.html', {'tabs': tabs,
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
    lesson = Lesson()
    lesson.title = _('undefined')
    lesson.course_id = course_id
    lesson.order = 0
    lesson.save()
    return HttpResponseRedirect(reverse('lesson_edit', args=(lesson.id,)))


def edit_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course
    tabs = [
        Tab(_('Main'), 'lesson_main', params=(lesson_id,)),
        Tab(_('Slides'), 'lesson_slides', params=(lesson_id,), is_active=True),
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
        Tab(_('Main'), 'slide_main', params=(slide_id,)),
        Tab(_('Compenents'), 'slide_components', params=(slide_id,), is_active=True),
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
        Tab(_('Main'), 'component_main', params=(component_id,)),
        Tab(_('Settings'), 'component_settings', params=(component_id,), is_active=True),
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

