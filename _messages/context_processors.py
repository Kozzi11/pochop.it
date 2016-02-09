from django.contrib.auth import get_user
from _messages.utils import MessageUtil
from pochopit.models import UserProfile


def messages(request):
    count_off_unseen_messages = 0
    user_mits = 0
    if request.user.is_authenticated():
        user = get_user(request)
        count_off_unseen_messages = MessageUtil.get_count_of_unseen_messages(user)
        user_mits = UserProfile.objects.get_or_create(user=user)[0].mits

    return {'count_off_unseen_messages': count_off_unseen_messages, 'user_mits': user_mits}
