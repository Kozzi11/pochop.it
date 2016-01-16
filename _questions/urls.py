from django.conf.urls import url

from . import views
from _questions.constants import URLS


urlpatterns = [
    url(r'^questions/$', views.questions, name=URLS.QUESTIONS),
    url(r'^questions/grid_data$', views.questions_grid_data, name=URLS.QUESTIONS_GRID_DATA),
    url(r'^questions/ask_question$', views.ask_question, name=URLS.ASK_QUESTION),
    url(r'^question/(.*)/(.*)$', views.view_question, name=URLS.VIEW_QUESTION),
    url(r'^question_t/(.*)/edit$', views.edit_question, name=URLS.EDIT_QUESTION),
    url(r'^question_t/(.*)/revision$', views.check_question_revision, name=URLS.REVISION_QUESTION),
    url(r'^answer/(.*)/edit$', views.edit_answer, name=URLS.EDIT_ANSWER),
    url(r'^answer/(.*)/revision/$', views.check_answer_revision, name=URLS.REVISION_ANSWER),
    url(r'^tags/find$', views.find_tags, name=URLS.FIND_TAGS),
    url(r'^tags/create', views.create_tag, name=URLS.CREATE_TAG),
    url(r'^vote/question/(.*)/up', views.vote_up_question, name=URLS.VOTE_UP_QUESTION),
    url(r'^vote/question/(.*)/down', views.vote_down_question, name=URLS.VOTE_DOWN_QUESTION),
    url(r'^vote/answer/(.*)/up', views.vote_up_answer, name=URLS.VOTE_UP_ANSWER),
    url(r'^vote/answer/(.*)/down', views.vote_down_answer, name=URLS.VOTE_DOWN_ANSWER),
]
