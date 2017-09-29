from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^users/(?P<user_id>[1-9][0-9]*)/$', user_page),
    url(r'^users/profile/$', profile),
    url(r'^users/profile/update/$', profile_update),
    url(r'^users/preference/$', preference),
    url(r'^users/preference/update/$', preference_update),
]