from django.conf.urls import url
from django.contrib import admin

from api import *
urlpatterns = [
    url(r'^$',index_page),
    url(r'^api/messages/$',ApiWallView.as_view()),
    url(r'^api/comments/$',ApiCommentView.as_view()),
]