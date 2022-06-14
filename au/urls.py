from django.urls import path, re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import re_path as url
from django.views.static import serve

from .views import *

urlpatterns = [
    path('register/', Register.as_view()),
    path('captcha/', Captcha.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('chpwd/', Chpwd.as_view()),
    path('update/', Update.as_view()),
    re_path('^user/(?P<pk>.*)$', UserQuery.as_view()),
    path('me/', MyQuery.as_view()),
    path('forget/', Forget.as_view()),
    path('chavatar/', Chavatar.as_view())
]