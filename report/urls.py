from django.urls import path, re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import re_path as url
from django.views.static import serve
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('list', login_required(List.as_view())),
    path('release', login_required(Release.as_view())),
    path('delete', login_required(Delete.as_view())),
    path('star', login_required(Star.as_view())),
    path('reply', login_required(Reply.as_view())),
]