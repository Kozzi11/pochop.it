from django.contrib.auth import get_user
from django.shortcuts import render


def get_count_of_notification(request):
    user = get_user(request.user)

