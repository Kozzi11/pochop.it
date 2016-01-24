from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    mits = models.BigIntegerField(default=0)
    businesscard = models.TextField(default='')


class MitTransaction(models.Model):

    TYPE_ADD_QUESTION = 1  # az alespon x lidi oznaci otazku za prospesnou
    TYPE_ADD_ANSWER = 2  # az alespon x lidi oznaci odpoved za prospesnou
    TYPE_VOTE_QUESTION = 3  # za kazdeho dalsiho cloveka ktery bude hlasovat, zastropovano (MAX_AMOUNT_VOTE_QUESTION)
    TYPE_VOTE_ANSWER = 4  # za kazdeho dalsiho cloveka ktery bude hlasovat, zastropovano (MAX_AMOUNT_VOTE_ANSWER)
    TYPE_EDIT_QUESTION = 5  # az bude editace uznana, schvalujici osoba rozhoduje jakou cast odmeny dostane
    TYPE_EDIT_ANSWER = 6  # az bude editace uznana, schvalujici osoba rozhoduje jakou cast odmeny dostane
    TYPE_APPROVE_QUESTION_EDIT = 7  # dostane odmenu vzdy
    TYPE_APPROVE_ANSWER_EDIT = 8  # dostane odmenu vzdy
    TYPE_FACEBOOK = 9  # uzivatel dostane odmenu za to, ze da sdilet pochopIT na svou stenu

    AMOUNT_ADD_QUESTION = 150  # odmena za otazku
    AMOUNT_ADD_ANSWER = 150  # odmena za odpoved
    VOTE_COUNT_ADD_QUESTION = 3  # pocet lidi co musi hlasovat aby se pricetla odmena za otazku
    VOTE_COUNT_ADD_ANSWR = 3  # pocet lidi co musi hlasovat aby se pricetla odmena za odpoved

    AMOUNT_VOTE_QUESTION = 2  # odmena za hlasovani
    AMOUNT_VOTE_ANSWER = 2  # odmena za hlasovani
    MAX_AMOUNT_VOTE_QUESTION = 20  # maximalni odmena za hlasovani k jedne otazce
    MAX_AMOUNT_VOTE_ANSWER = 20  # maximalni odmena za hlasovani k jedne odpovedi
    DAY_VOTE_LIMIT = 10  # denní limit hlasování

    AMOUNT_EDIT_QUESTION_SMALL = 10  # mala odmena za editaci otazky
    AMOUNT_EDIT_QUESTION_MIDDLE = 30  # strendni odmena za editaci otazky
    AMOUNT_EDIT_QUESTION_FULL = 50  # plna odmena za editaci otazky
    AMOUNT_EDIT_ANSWER_SMALL = 10  # mala odmena za editaci odpovedi
    AMOUNT_EDIT_ANSWER_MIDDLE = 30  # strendni odmena za editaci odpovedi
    AMOUNT_EDIT_ANSWER_FULL = 50  # plna odmena za editaci odpovedi

    AMOUNT_APPROVE_QUESTION_EDIT = 10  # odmena za revizi uprav otazky
    AMOUNT_APPROVE_ANSWER_EDIT = 10  # odmena za revizi uprav odpovedi

    AMOUNT_FACEBOOK = 300  # odmena za umisteni pochopIT na svoji stenu na facebooku

    user_to = models.ForeignKey(User)
    user_from = models.ForeignKey(User, related_name='transaction_user_from')
    type = models.IntegerField()
    amount = models.IntegerField()
    note = models.CharField(max_length=255, null=True)
    to_before_trans = models.IntegerField()  # stav uctu odchoziho uctu, pred provedenim transakce
    from_before_trans = models.IntegerField()  # stav ciloveho uctu, pred provedenim transakce
    context_info = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
