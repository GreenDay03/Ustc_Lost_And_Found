from datetime import date, datetime, timedelta
import random
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from .models import *
from django.core.files.storage import default_storage
from django.contrib import auth
from django.core.mail import send_mail

def dict_clear(dic : dict, invalid_keys={'',None}):
    '''把字典里某些键不合要求的项目都清除了'''
    return dict([(x, y) for x, y in dic.items() if y not in invalid_keys])

class ViewBase(View):
    def fail(self,msg=''):
        return JsonResponse({
            "result" : "fail",
            "msg" : msg
        })
    SUCCESS = JsonResponse({  "result" : "success"   })


def check_email(email:str):
    '''禁止注册非妮可邮箱。'''
    return email.endswith('@mail.ustc.edu.cn') or email.endswith('@ustc.edu.cn')

def check_captcha(email, captcha, auto_del=True):
    '''检查验证码和邮箱匹不匹配。auto_del指验证成功就删掉信息'''
    try:
        info = CaptchaInfo.objects.get(email=email) #这个地方出错会跳出的
    except Exception:
        return False
    dic = model_to_dict(info)
    print(dic['end_time'] >= datetime.now())
    print(dic['captcha'] == captcha)
    if dic['end_time'] >= datetime.now() and dic['captcha'] == captcha:   #时间还没过期
        if auto_del:
            info.delete()
        return True
    else:
        return False

def check_password(password:str):
    '''检查密码是否合法'''
    if not isinstance(password,str):
        return False
    if len(password) < 6 or len(password) > 20:
        return False
    return True

class Register(ViewBase):
    '''
        注意有3点不太一致：
        HTTP参数中stu_id对应数据库里面的username
        HTTP参数中username对应数据库里面的first_name
        HTTP参数中realname对应数据库里面的last_name
        （主要是为了利用系统自带的各种东西，我承认我偷懒了）
    '''
    def post(self, request):
        if request.user.is_authenticated:
            return self.fail('您已登录，不能注册')
        captcha = request.POST.get('captcha')
        email = request.POST.get('email')
        stu_id = request.POST.get('stu_id')
        password = request.POST.get('password')
        username = request.POST.get('username')
        if not check_email(email):
            return self.fail('邮箱不合法')
        if UstcUser.objects.filter(email=email):
            return self.fail('这个邮箱已经注册过了')
        if not check_password(password):
            return self.fail('密码不合法')
        if not check_captcha(email, captcha):
            return self.fail('验证码不对')
        UstcUser.objects.create_user(username=stu_id,password=password,email=email,first_name=username)
        return self.SUCCESS

class Captcha(ViewBase):
    def random_str(self,random_length=6):
        '''
        生成随机字符串作为验证码
        :param random_length: 字符串长度,默认为6
        :return: 随机字符串
        '''
        string = ''
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        length = len(chars) - 1
        # random = Random()
        # 设置循环每次取一个字符用来生成随机数
        for i in range(random_length):
            string += chars[random.randint(0, length)]
        return string
        #这个函数是从CSDN上复制过来的


    def post(self, request):
        email = request.POST.get('email')
        if not check_email(email):
            return self.fail('邮箱不合法')
        captcha = self.random_str()
        send_mail(
            '中科大权益柜验证码',
            f'同学你好：\n\t感谢你使用中科大权益柜。你的验证码是：{captcha}。请您在10分钟内完成验证。谢谢。\n\t中科大权益柜项目组。',
            None,
            [email]
        )
        ret = CaptchaInfo.objects.filter(email=email)
        if ret.count() != 1:
            ret.delete()    #管他发生什么情况，不等于1，一律重来。
            CaptchaInfo.objects.create(email=email,captcha=captcha,end_time=datetime.now()+timedelta(minutes=10))
        else:
            ret.update(captcha=captcha,end_time=datetime.now()+timedelta(minutes=10))
        return self.SUCCESS

class Login(ViewBase):
    def post(self, request):
        if request.user.is_authenticated:
            return self.fail('您已登录')
        try:
            print(request.POST)
            stu_id = request.POST.get('stu_id')
            password = request.POST.get('password')
            print(stu_id,password)
            user = auth.authenticate(username=stu_id, password=password)
            if user:
                auth.login(request, user)
                return self.SUCCESS
            else:
                return self.fail('用户名或密码错误')
        except Exception:
            return self.fail('用户名或密码错误')

class Logout(ViewBase):
    def post(self, request):
        if not request.user.is_authenticated:
            return self.fail('您已登出')
        else:
            auth.logout(request)
            return self.SUCCESS


class Chpwd(ViewBase):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return self.fail('您未登录')
        old = request.POST.get('old')
        new = request.POST.get('new')
        if not user.check_password(old):
            return self.fail('原密码不对')
        if not check_password(new):
            return self.fail('密码不合法')
        user.set_password(new)
        user.save()
        return self.SUCCESS

class Update(ViewBase):
    def post(self, request):
        if not request.user.is_authenticated:
            return self.fail('您还未登录')
        pk = request.user.id
        ret = UstcUser.objects.filter(pk=pk)
        if ret.count() != 1:
            return self.fail('找不到这个用户')
        update_info = {
            'last_name' : request.POST.get('realname'),
            'first_name' : request.POST.get('username'),
            'mobile' : request.POST.get('mobile'),
            'qq' : request.POST.get('qq')
        }
        ret.update(**dict_clear(update_info))
        return self.SUCCESS

class UserQuery(ViewBase):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return self.fail('您未登录')
        #stu_id = self.kwargs['stu_id']
        try:
            account = UstcUser.objects.get(pk=pk)
        except:
            return self.fail('找不到这个用户')
        ret = {'result' : 'success'}
        ret['id'] = pk
        ret['stu_id'] = account.username
        ret['email'] = account.email
        ret['mobile'] = account.mobile
        ret['username'] = account.first_name
        ret['realname'] = account.last_name
        ret['qq'] = account.qq
        ret['avatar'] = account.avatar
        return JsonResponse(dict_clear(ret))

class MyQuery(UserQuery):
    def get(self, request):
        if not request.user.is_authenticated:
            return self.fail('您未登录') 
        return super().get(request, request.user.id)

class Forget(ViewBase):
    def post(self, request):
        email = request.POST.get('email')
        captcha = request.POST.get('captcha')
        password = request.POST.get('password')
        if not check_email(email):
            return self.fail('邮箱不合法')
        try:
            account = UstcUser.objects.get(email=email)
        except:
            return self.fail('邮箱还没注册')
        if not check_password(password):
            return self.fail('密码不合法')
        if not check_captcha(email, captcha):
            return self.fail('验证码不对')
        account.set_password(password)
        account.save()
        return self.SUCCESS