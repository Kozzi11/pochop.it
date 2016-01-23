from django.conf.urls import url

from . import views
from _questions.constants import URLS


urlpatterns = [
    url(r'^questions/administration$', views.administration, name=URLS.ADMINISTRATION),
    url(r'^questions/$', views.questions, name=URLS.QUESTIONS),
    url(r'^questions/grid_data$', views.questions_grid_data, name=URLS.QUESTIONS_GRID_DATA),
    url(r'^questions/ask_question$', views.ask_question, name=URLS.ASK_QUESTION),
    url(r'^questions/(.*)/(.*)$', views.view_question, name=URLS.VIEW_QUESTION),
    url(r'^question/(.*)/edit$', views.edit_question, name=URLS.EDIT_QUESTION),
    url(r'^question/(.*)/revision$', views.authorize_question_edit, name=URLS.AUTHORIZE_QUESTION_EDIT),
    url(r'^question/add_comment$', views.question_add_comment, name=URLS.COMMENT_QUESTION),
    url(r'^question/(.*)/scrap$', views.question_scrap, name=URLS.SCRAP_QUESTION),
    url(r'^question/(.*)/scrap_comment$', views.question_comment_scrap, name=URLS.SCRAP_QUESTION_COMMENT),
    url(r'^answer/(.*)/edit$', views.edit_answer, name=URLS.EDIT_ANSWER),
    url(r'^answer/(.*)/revision/$', views.authorize_answer_edit, name=URLS.AUTHORIZE_ANSWER_EDIT),
    url(r'^answer/add_comment$', views.answer_add_comment, name=URLS.COMMENT_ANSWER),
    url(r'^answer/(.*)/scrap$', views.answer_scrap, name=URLS.SCRAP_ANSWER),
    url(r'^answer/(.*)/scrap_comment$', views.answer_comment_scrap, name=URLS.SCRAP_ANSWER_COMMENT),
    url(r'^tags/find$', views.find_tags, name=URLS.FIND_TAGS),
    url(r'^tags/create$', views.create_tag, name=URLS.CREATE_TAG),
    url(r'^vote/question/(.*)/up$', views.vote_up_question, name=URLS.VOTE_UP_QUESTION),
    url(r'^vote/question/(.*)/down$', views.vote_down_question, name=URLS.VOTE_DOWN_QUESTION),
    url(r'^vote/answer/(.*)/up$', views.vote_up_answer, name=URLS.VOTE_UP_ANSWER),
    url(r'^vote/answer/(.*)/down$', views.vote_down_answer, name=URLS.VOTE_DOWN_ANSWER),
]
