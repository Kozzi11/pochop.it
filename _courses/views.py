from django.shortcuts import render


def courses(request, tab_name):
    tabs = {
        'in_progress': tab_name == 'in_progress',
        'all': tab_name == 'all',
        'completed': tab_name == 'completed',
        'my_courses': tab_name == 'my_courses',
    }
    template_name = '_courses/' + tab_name + '.html'
    return render(request, template_name, {'tabs': tabs})
