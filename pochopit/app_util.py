from django.contrib.auth.models import User
from pochopit.models import MitTransaction


class AppUtil:

    system_user = None

    @staticmethod
    def process_transaction(user_from=None, user_to=None, amount=None, trans_type=None, context_info=None, note=None):
        if user_from and user_to and trans_type and amount:
            transaction = MitTransaction()
            transaction.user_to = user_to
            transaction.user_from = user_from
            transaction.amount = amount
            transaction.type = trans_type
            transaction.context_info = context_info
            transaction.note = note
            transaction.to_before_trans = user_to.userprofile.mits
            transaction.from_before_trans = user_from.userprofile.mits

            user_from.userprofile.mits -= amount
            user_to.userprofile.mits += amount
            # todo - osetrit radeji primo db transakci at se to nepokaka

            transaction.save()
            user_from.userprofile.save()
            user_to.userprofile.save()
        else:
            raise NameError('Can not process transaction some invalid parameters')

    @staticmethod
    def get_system_user():
        if AppUtil.system_user is None:
            AppUtil.system_user = User.objects.get(id=1)
        return AppUtil.system_user
