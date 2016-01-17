from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required
from _questions.constants import URLS


urlpatterns = [
    url(r'^questions/$', views.questions, name=URLS.QUESTIONS),
    url(r'^questions/grid_data$', views.questions_grid_data, name=URLS.QUESTIONS_GRID_DATA),
    url(r'^questions/ask_question$', login_required(views.ask_question), name=URLS.ASK_QUESTION),
    url(r'^question/(.*)/(.*)$', views.view_question, name=URLS.VIEW_QUESTION),
    url(r'^question_t/(.*)/edit$', login_required(views.edit_question), name=URLS.EDIT_QUESTION),
    url(r'^question_t/(.*)/revision$', login_required(views.check_question_revision), name=URLS.REVISION_QUESTION),
    url(r'^question_t/add_comment', login_required(views.question_add_comment), name=URLS.COMMENT_QUESTION),
    url(r'^answer/(.*)/edit$', login_required(views.edit_answer), name=URLS.EDIT_ANSWER),
    url(r'^answer/(.*)/revision/$', login_required(views.check_answer_revision), name=URLS.REVISION_ANSWER),
    url(r'^answer/add_comment', login_required(views.answer_add_comment), name=URLS.COMMENT_ANSWER),
    url(r'^tags/find$', login_required(views.find_tags), name=URLS.FIND_TAGS),
    url(r'^tags/create', login_required(views.create_tag), name=URLS.CREATE_TAG),
    url(r'^vote/question/(.*)/up', login_required(views.vote_up_question), name=URLS.VOTE_UP_QUESTION),
    url(r'^vote/question/(.*)/down', login_required(views.vote_down_question), name=URLS.VOTE_DOWN_QUESTION),
    url(r'^vote/answer/(.*)/up', login_required(views.vote_up_answer), name=URLS.VOTE_UP_ANSWER),
    url(r'^vote/answer/(.*)/down', login_required(views.vote_down_answer), name=URLS.VOTE_DOWN_ANSWER),
]
