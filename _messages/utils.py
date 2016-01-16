from _messages.models import Message


class MessageUtil:

    @staticmethod
    def get_count_of_unseen_messages(user):
        return Message.objects.filter(user=user, status=Message.STATUS_UNSEEN).count()
