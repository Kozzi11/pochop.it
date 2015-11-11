from django.shortcuts import render


def courses(request, tab_name):
    return render(request, '_courses/courses.html', {'tab_name': tab_name})
