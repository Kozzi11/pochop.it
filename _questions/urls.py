from django.conf.urls import url

from . import views

QUESTIONS = 'questions'
QUESTIONS_GRID_DATA = 'questions_grid_data'
ASK_QUESTION = 'ask_question'
FIND_TAGS = 'find_tags'
CREATE_TAG = 'create_tag'

urlpatterns = [
    url(r'^questions/$', views.questions, name=QUESTIONS),
    url(r'^questions/grid_data$', views.questions_grid_data, name=QUESTIONS_GRID_DATA),
    url(r'^questions/ask_question$', views.ask_question, name=ASK_QUESTION),
    url(r'^tags/find$', views.find_tags, name=FIND_TAGS),
    url(r'^tags/create', views.create_tag, name=CREATE_TAG),
]
