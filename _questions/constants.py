
class URLS:
    ADMINISTRATION = 'administration'
    QUESTIONS = 'questions'
    QUESTIONS_GRID_DATA = 'questions_grid_data'
    ASK_QUESTION = 'ask_question'
    EDIT_QUESTION = 'edit_question'
    COMMENT_QUESTION = 'comment_question'
    COMMENT_ANSWER = 'comment_answer'
    EDIT_ANSWER = 'edit_answer'
    VIEW_QUESTION = 'view_question'
    AUTHORIZE_QUESTION_EDIT = 'auth_questino_edit'
    AUTHORIZE_ANSWER_EDIT = 'auth_answer_edit'
    FIND_TAGS = 'find_tags'
    CREATE_TAG = 'create_tag'
    VOTE_UP_QUESTION = 'vote_up_question'
    VOTE_DOWN_QUESTION = 'vote_down_question'
    VOTE_UP_ANSWER = 'vote_up_answer'
    VOTE_DOWN_ANSWER = 'vote_down_answer'
    SCRAP_QUESTION = 'scrap_question'
    SCRAP_ANSWER = 'scrap_answer'
    SCRAP_QUESTION_COMMENT = 'scrap_question_comment'
    SCRAP_ANSWER_COMMENT = 'scrap_answer_comment'


class PERMISSION:
    AUTHORIZE_QUESTION_EDIT = '_questions.change_questionrevision'
    AUTHORIZE_ANSWER_EDIT = '_questions.change_answerrevision'
    ADD_TAG = '_questions.change_tag'


class PERMISSION_GROUPS:
    SUPERVISOR = 'supervisor'
