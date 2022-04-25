from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class UserInfoAdmin(UserAdmin):
	# 这是在管理页面中想要显示的内容
    list_display = ['username', 'email', 'date_joined', 'last_login']
	# 分页
    list_per_page = 10
    # 设置 只读 的字段
    readonly_fields = ['date_joined', 'last_login']
    # 后台显示的字段
    fieldsets = [
               (None, {'fields':['username', 'password', 'email', 'is_staff', 'is_superuser']}),
               ('用户活跃信息', {'fields': ['date_joined', 'last_login']}),
    ]
# Register your models here.
admin.site.register(UstcUser, UserAdmin)
admin.site.register(CaptchaInfo)