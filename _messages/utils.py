from _messages.models import Message


class MessageUtil:

    @staticmethod
    def get_count_of_unseen_messages(user):
        return Message.objects.filter(user=user, status=Message.STATUS_UNSEEN).count()

    @staticmethod
    def send_message(sender, recipient, message_type, text='', params=None):
        message = Message()
        message.user = recipient
        message.sender = sender
        message.type = message_type
        message.status = 0
        message.text = text
        message.params = params
        message.save()
