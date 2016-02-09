from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from _auth.constants import URLS
from _auth.forms import LoginForm
from _homepage.constants import URLS as HOMEPAGE_URLS

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': '_auth/login.html', 'authentication_form': LoginForm},
        name=URLS.SIGN_IN),
    url(r'^logout/$', auth_views.logout, {'next_page': HOMEPAGE_URLS.HOMEPAGE}),
    url(r'^sing_up/$', views.sign_up, name=URLS.SIGN_UP),
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': '_auth/password_reset.html', 'post_reset_redirect': URLS.PASSWORD_RESET_REDIRECT},
        name=URLS.PASSWORD_RESET),

    url(r'^password_reset/done$', views.password_reset_done, name=URLS.PASSWORD_RESET_REDIRECT),
    url(r'^profile/(.*)/$', views.profile, name=URLS.PROFILE),
    url(r'^my_profile/$', views.my_profile, name=URLS.MY_PROFILE),
    url(r'^my_profile/edit$', views.my_profile_edit, name=URLS.MY_PROFILE_EDIT),
]
