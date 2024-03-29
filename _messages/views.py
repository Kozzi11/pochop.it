from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from _messages.models import Message


@login_required
def get_notification_list(request):
    user = get_user(request)
    notifications = Message.objects.filter(user=user).order_by('-created')
    for notif in notifications:
        notif.status = Message.STATUS_SEEN
        notif.save()

    if notifications.count() > 10:
        notifications = notifications[:10]
    return render(request, '_messages/notifications.html', {'notifications': notifications})
