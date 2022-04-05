from django.urls import path, re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

from .views import *

urlpatterns = [
    path('register/', Register.as_view),
    path('captcha/', Captcha.as_view),
    path('login/', Login.as_view),
    path('logout/', Logout.as_view),
    path('chpwd/', Chpwd.as_view),
    path('update/', Update.as_view),
#    re_path(r'^user/(?P<year>\d+)/$', get_user),
#    path('me/', get_self)
]