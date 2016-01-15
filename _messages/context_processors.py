from django.contrib.auth import get_user

from _messages.utils import MessageUtil


def messages_processor(request):
    count_off_unseen_messages = MessageUtil.get_count_of_unseen_messages(request.user.id)
    return {'count_off_unseen_messages': count_off_unseen_messages}