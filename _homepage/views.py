from django.shortcuts import render


def homepage(request):
    return render(request, '_homepage/homepage.html')


def about(request):
    return render(request, '_homepage/about.html')
