from django.conf.urls import url

from . import views

QUESTIONS = 'questions'
QUESTIONS_GRID_DATA = 'questions_grid_data'
ASK_QUESTION = 'ask_question'
VIEW_QUESTION = 'view_question'
FIND_TAGS = 'find_tags'
CREATE_TAG = 'create_tag'
VOTE_UP_QUESTION = 'vote_up_question'
VOTE_DOWN_QUESTION = 'vote_down_question'
VOTE_UP_ANSWER = 'vote_up_answer'
VOTE_DOWN_ANSWER = 'vote_down_answer'

urlpatterns = [
    url(r'^questions/$', views.questions, name=QUESTIONS),
    url(r'^questions/grid_data$', views.questions_grid_data, name=QUESTIONS_GRID_DATA),
    url(r'^questions/ask_question$', views.ask_question, name=ASK_QUESTION),
    url(r'^questions/(.*)/view$', views.view_question, name=VIEW_QUESTION),
    url(r'^tags/find$', views.find_tags, name=FIND_TAGS),
    url(r'^tags/create', views.create_tag, name=CREATE_TAG),
    url(r'^vote/question/(.*)/up', views.vote_up_question, name=VOTE_UP_QUESTION),
    url(r'^vote/question/(.*)/down', views.vote_down_question, name=VOTE_DOWN_QUESTION),
    url(r'^vote/answer/(.*)/up', views.vote_up_answer, name=VOTE_UP_ANSWER),
    url(r'^vote/answer/(.*)/down', views.vote_down_answer, name=VOTE_DOWN_ANSWER),
]
