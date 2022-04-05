from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager

class UserManager(BaseUserManager): #自定义Manager管理器
    def _create_user(self,username,password,email,**kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        user = self.model(username=username,email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,username,password,email,**kwargs): # 创建普通用户
        kwargs['is_superuser'] = False
        return self._create_user(username,password,email,**kwargs)

    def create_superuser(self,username,password,email,**kwargs): # 创建超级用户
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username,password,email,**kwargs)
    #以上代码是直接从CSDN上复制过来的
    #https://blog.csdn.net/weixin_44951273/article/details/101028522
    #原作者：小泽十一章    

# Create your models here.
class UstcUser(AbstractUser):
    qq = models.CharField(max_length=13, blank=True)
    mobile = models.CharField(max_length=13, blank=True)
    objects = UserManager()
    avatar = models.FileField(blank=True)   #avatar的意思是头像


class CaptchaInfo(models.Model):
    email = models.EmailField()
    captcha = models.CharField(max_length=6)
    end_time = models.TimeField()
