from django.contrib.auth import get_user
from django.shortcuts import render
from _messages.models import Message


def get_notification_list(request):
    user = get_user(request)
    notifications = Message.objects.filter(user=user).order_by('-created')
    for notif in notifications:
        notif.status = Message.STATUS_SEEN
        notif.save()

    if notifications.count() > 15:
        notifications = notifications[:15]
    return render(request, '_messages/notifications.html', {'notifications': notifications})
