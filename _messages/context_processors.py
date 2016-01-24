from django.contrib.auth import get_user
from _messages.utils import MessageUtil


def messages(request):
    count_off_unseen_messages = 0
    user_mits = 0
    if request.user.is_authenticated():
        user = get_user(request)
        count_off_unseen_messages = MessageUtil.get_count_of_unseen_messages(user)
        user_mits = user.userprofile.mits

    return {'count_off_unseen_messages': count_off_unseen_messages, 'user_mits': user_mits}
