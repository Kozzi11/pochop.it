from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from _courses import urls as course_urls

from _courses.forms import ComponentForm
from _courses.models import ComponentData, ComponentConfig
from pochopit.viewcomponents.context_bar_item import ContextBarItem


def html(request, component_data_id):
    component_data = ComponentData.objects.get(id=component_data_id)

    if component_data.componentconfig_set.filter(key=ComponentConfig.KEY_CONTENT).exists():
        content_config = component_data.componentconfig_set.get(key=ComponentConfig.KEY_CONTENT)
    else:
        content_config = ComponentConfig()
        content_config.key = ComponentConfig.KEY_CONTENT
        content_config.value = ''
        content_config.componentData = component_data

    if request.method == 'POST':
        form = ComponentForm(request.POST, instance=component_data)
        form.save()
        content_config.value = form.cleaned_data['content']
        content_config.save()
        url = reverse(course_urls.COURSE_EDIT,
                      args=(component_data.slide.lesson.course_id,)) + "#" + reverse(course_urls.SLIDE_EDIT_CONTENT,
                                                                                     args=(component_data.slide_id,))
        return HttpResponseRedirect(url)
    else:
        form = ComponentForm(instance=component_data, initial={'content': content_config.value})

    context_bar_items = [
        ContextBarItem(component_data.slide.lesson.title),
        ContextBarItem(component_data.slide.title),
        ContextBarItem(component_data.title),
    ]
    return render(request, '_components/html/html_settings.html',
                  {'component_data_id': component_data_id, 'form': form, 'context_bar_items': context_bar_items})
