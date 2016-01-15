from _messages.models import Message


class MessageUtil:

    @staticmethod
    def get_count_of_unseen_messages(user_id):
        return Message.objects.filter(user_id=user_id, status=Message.STATUS_UNSEEN).count()
