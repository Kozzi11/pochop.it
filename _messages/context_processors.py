from django.contrib.auth import get_user
from _messages.utils import MessageUtil


def messages(request):
    user = get_user(request)
    count_off_unseen_messages = MessageUtil.get_count_of_unseen_messages(user)
    return {'count_off_unseen_messages': count_off_unseen_messages}
