from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from _auth.constants import URLS
from _homepage.constants import URLS as HOMEPAGE_URLS

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': '_auth/login.html'}, name=URLS.SIGN_IN),
    url(r'^logout/$', auth_views.logout, {'next_page': HOMEPAGE_URLS.HOMEPAGE}),
    url(r'^sing_up/$', views.sign_up, name=URLS.SIGN_UP),
    url(r'^profile/(.*)/$', views.profile, name=URLS.PROFILE),
    url(r'^my_profile/$', views.my_profile, name=URLS.MY_PROFILE),
    url(r'^my_profile/edit$', views.my_profile_edit, name=URLS.MY_PROFILE_EDIT),
]
