from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', inbox),
    url(r'^new/(?P<user_id>[1-9][0-9]*)/$', new),
    url(r'^new/(?P<user_id>[1-9][0-9]*)/create/$', create_conversation),
    url(r'^(?P<conversation_id>[1-9][0-9]*)/$', conversation),
    url(r'^(?P<conversation_id>[1-9][0-9]*)/add/$', add_message),
]