from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.contrib.auth import get_user
from _components.models.ComponentBuilder import ComoponentBuilder
from _courses import urls
from _courses.forms import CourseForm, LessonForm, SlideForm, ComponentForm
from _courses.models import Course, Lesson, Slide, ComponentData
from eztables.views import DatatablesView
from pochopit.viewcomponents.context_bar_item import ContextBarItem
from pochopit.viewcomponents.tab import Tab
from pochopit.viewcomponents.tab_group import TabGroup
from pochopit.viewcomponents.tabs_manager import TabsManager


def courses(request):
    tabs_manager = TabsManager(request)
    tabs_manager.add_tab(
        Tab(_('All'), reverse(urls.COURSES_ALL), urls.COURSES_ALL, is_active=True)
    )
    tabs_manager.add_tab(
        Tab(_('In progress'), reverse(urls.COURSES_IN_PROGRESS), urls.COURSES_IN_PROGRESS, buddge_number=2)
    )
    tabs_manager.add_tab(
        Tab(_('Completed'), reverse(urls.COURSES_COMPLETED), urls.COURSES_COMPLETED, buddge_number=8)
    )
    tabs_manager.add_tab(
        Tab(_('My courses'), reverse(urls.COURSES_MY), urls.COURSES_MY, buddge_number=3)
    )

    return render(request, '_courses/courses_base.html', {'tabs': tabs_manager.get_tabs()})


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
    course.title = _('New course')
    course.save()

    lesson = Lesson()
    lesson.title = _('Lesson') + ' 1'
    lesson.course = course
    lesson.order = 0
    lesson.save()

    slide = Slide()
    slide.lesson = lesson
    slide.title = _('Slide') + ' 1'
    slide.order = 0
    slide.save()

    component_data = ComponentData()
    component_data.title = _('Component') + ' 1'
    component_data.slide = slide
    component_data.type = ComponentData.TYPE_HTML
    component_data.order = 0
    component_data.save()

    url = reverse(urls.COURSE_EDIT, args=(course.id,)) + "#" + "#" + reverse(urls.SLIDE_EDIT_CONTENT,
                                                                             args=(slide.id,))
    return HttpResponseRedirect(url)


def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    url = reverse(urls.COURSES) + "#" + reverse(urls.COURSES_MY)
    return HttpResponseRedirect(url)


def edit_course(request, course_id):
    tabs_manager = TabsManager(request)
    course = Course.objects.get(id=course_id)

    js_after_ajax = 'location.reload();'

    courses_tab_group = TabGroup(course.title)
    courses_tab_group.add_action_button(reverse(urls.COURSE_MAIN, args=(course.id,)), 'pencil',
                                        short_name=urls.COURSE_MAIN + str(course_id))
    courses_tab_group.add_action_button(reverse(urls.LESSON_NEW, args=(course.id,)), 'plus',
                                        short_name=urls.LESSON_NEW + str(course_id), change_content=False,
                                        js_after=js_after_ajax)

    lesson_set = course.lesson_set.all()
    lesson_count = len(lesson_set)
    i = 1
    for lesson in lesson_set:
        lessons_tab_group = TabGroup(lesson.title)
        lessons_tab_group.add_action_button(reverse(urls.LESSON_MAIN, args=(lesson.id,)), 'pencil',
                                            short_name=urls.LESSON_MAIN + str(lesson.id))
        lessons_tab_group.add_action_button(reverse(urls.SLIDE_NEW, args=(lesson.id,)), 'plus',
                                            short_name=urls.SLIDE_NEW + str(lesson.id), change_content=False,
                                            js_after=js_after_ajax)
        slide_set = lesson.slide_set.all()
        slide_count = len(slide_set)
        k = 1
        for slide in slide_set:
            slides_tab = Tab(slide.title, reverse(urls.SLIDE_EDIT_CONTENT, args=(slide.id,)),
                             urls.SLIDE_EDIT_CONTENT + str(slide.id), i == lesson_count and k == slide_count)

            slides_tab.add_action_button(reverse(urls.SLIDE_MAIN, args=(slide.id,)), 'pencil',
                                         short_name=urls.SLIDE_MAIN + str(slide.id))

            lessons_tab_group.add_tab(slides_tab)
            k += 1

        courses_tab_group.add_tab_group(lessons_tab_group)
        i += 1

    tabs_manager.add_tab_group(courses_tab_group)

    return render(request, '_courses/courses_base.html', {'tabs': tabs_manager.get_tabs()})


def course_main_tab(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        form.save()
        return HttpResponseRedirect(reverse(urls.COURSE_EDIT, args=(course_id,)))
    else:
        form = CourseForm(instance=course)

    context_bar_items = [
        ContextBarItem(course.title),
    ]

    return render(request, '_courses/course/main.html',
                  {'form': form, 'course_id': course_id, 'context_bar_items': context_bar_items})


def course_lessons_tab(request, course_id):
    return render(request, '_courses/course/lessons.html', {'course_id': course_id})


def new_lesson(request, course_id):
    course = Course.objects.get(id=course_id)

    lesson_count = course.lesson_set.count()
    lesson = Lesson()
    lesson.title = _('Lesson') + ' ' + str(lesson_count + 1)
    lesson.course = course
    lesson.order = lesson_count
    lesson.save()

    slide = Slide()
    slide.lesson = lesson
    slide.title = _('Slide') + ' 1'
    slide.order = 0
    slide.save()

    component_data = ComponentData()
    component_data.title = _('Component') + ' 1'
    component_data.slide = slide
    component_data.type = ComponentData.TYPE_HTML
    component_data.order = 0
    component_data.save()
    return HttpResponse()


def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    lesson.delete()
    url = reverse(urls.COURSE_EDIT, args=(lesson.course.id,))
    return HttpResponseRedirect(url)


def edit_lesson(request, lesson_id):
    tabs = [
        Tab(_('Main'), reverse(urls.LESSON_MAIN, args=(lesson_id,)), urls.LESSON_MAIN),
    ]

    return render(request, '_courses/courses_base.html', {'tabs': tabs})


def lesson_main_tab(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        form.save()
        last_slide_id = lesson.slide_set.first().id
        url = reverse(urls.COURSE_EDIT, args=(lesson.course.id,)) + "#" + reverse(urls.SLIDE_EDIT_CONTENT,
                                                                                  args=(last_slide_id,))
        return HttpResponseRedirect(url)
    else:
        form = LessonForm(instance=lesson)

    context_bar_items = [
        ContextBarItem(lesson.title),
    ]
    return render(request, '_courses/lesson/main.html',
                  dict(form=form, lesson_id=lesson_id, context_bar_items=context_bar_items))


def new_slide(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    slide_count = lesson.slide_set.count()

    slide = Slide()
    slide.lesson = lesson
    slide.title = _('Slide') + ' ' + str(slide_count + 1)
    slide.order = slide_count
    slide.save()

    component_data = ComponentData()
    component_data.title = _('Component') + ' 1'
    component_data.slide = slide
    component_data.type = ComponentData.TYPE_HTML
    component_data.order = 0
    component_data.save()
    return HttpResponse(reverse(urls.SLIDE_EDIT_CONTENT, args=(slide.id,)))


def delete_slide(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    slide.delete()
    url = reverse(urls.COURSE_EDIT, args=(slide.lesson.course_id,))
    return HttpResponseRedirect(url)


def slide_main_tab(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    if request.method == 'POST':
        form = SlideForm(request.POST, instance=slide)
        form.save()
        url = reverse(urls.COURSE_EDIT, args=(slide.lesson.course_id,)) + "#" + reverse(urls.SLIDE_EDIT_CONTENT,
                                                                                        args=(slide_id,))
        return HttpResponseRedirect(url)
    else:
        form = SlideForm(instance=slide)

    context_bar_items = [
        ContextBarItem(slide.lesson.title),
        ContextBarItem(slide.title),
    ]
    return render(request, '_courses/slide/main.html',
                  dict(form=form, slide_id=slide_id, context_bar_items=context_bar_items))


def edit_slide_content(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    component_data_set = slide.componentdata_set.all().order_by('order')
    components = []
    for component_data in component_data_set:
        components.append(ComoponentBuilder.prepare_component(component_data))

    context_bar_items = [
        ContextBarItem(slide.lesson.title, ''),
        ContextBarItem(slide.title, '#')
    ]
    return render(request, '_courses/slide/content.html',
                  {'slide_id': slide_id, 'components': components, 'context_bar_items': context_bar_items})


def new_component(request, slide_id):
    slide = Slide.objects.get(id=slide_id)
    component_count = slide.componentdata_set.count()
    component_data = ComponentData()
    component_data.title = _('Component') + ' ' + str(component_count + 1)
    component_data.slide = slide
    component_data.type = ComponentData.TYPE_HTML
    component_data.order = component_count
    component_data.save()
    return HttpResponse()


def delete_component(request, component_id):
    component_data = ComponentData.objects.get(id=component_id)
    component_data.delete()
    url = reverse(urls.COURSE_EDIT, args=(component_data.slide.lesson.course_id,))
    return HttpResponseRedirect(url)


def component_settings_tab(request, component_id):
    return render(request, '_courses/component/settings.html', {'component_id': component_id})


def component_change_order(request, component_data_id, step):
    step = int(step)
    component_data = ComponentData.objects.get(id=component_data_id)
    old_position = component_data.order
    new_positon = old_position + int(step)
    count_of_components = component_data.slide.componentdata_set.count()

    if step > 0 and new_positon > count_of_components:
        return HttpResponse()
    elif step < 0 and new_positon < 0:
        return HttpResponse()

    for data in component_data.slide.componentdata_set.all():
        if data.order == new_positon:
            data.order = old_position
            data.save()
            break

    component_data.order = new_positon
    component_data.save()
    return HttpResponse()


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
