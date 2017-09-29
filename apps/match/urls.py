from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^(?P<page_num>[1-9][0-9]*)/$', index),
]