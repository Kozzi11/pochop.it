from django.contrib.auth import get_user
from _messages.utils import MessageUtil


def messages(request):
    count_off_unseen_messages = 0
    user_minutes = 0
    if request.user.is_authenticated():
        user = get_user(request)
        count_off_unseen_messages = MessageUtil.get_count_of_unseen_messages(user)
        user_minutes = user.usersetting.minutes / 10

    return {'count_off_unseen_messages': count_off_unseen_messages, 'user_minutes': user_minutes}
