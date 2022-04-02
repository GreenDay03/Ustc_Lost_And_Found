from django.urls import path, re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

from .views import *

urlpatterns = [
    path('list/', List.as_view()),
    path('release/', Release.as_view()),
    path('delete/', Delete.as_view()),
    path('pick/', Pick.as_view()),
    path('reply/', Reply.as_view()),
    path('confirm/', Confirm.as_view())
]