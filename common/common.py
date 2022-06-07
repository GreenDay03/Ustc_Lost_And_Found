from django.views.generic.base import View
from django.http import JsonResponse
import random
import os.path
from django.core.files.base import ContentFile

PICTURE_SUFFIX = ['.jpg', '.jpeg', '.png', '.gif', '.ico', '.bmp']
def process_file(file,maxsize=10*(2**20),allow_suffix=PICTURE_SUFFIX):
    '''
        request
        处理文件，返回一个元组表示：file_name, file_content, file_suffix
        有错误则返回3个None
        maxsize=0表示不设置maxsize,allow_suffix=None表示都可以
    '''
    if not file:
        return None, None, None
    file_suffix = os.path.splitext(file.name)[-1].lower()
    if allow_suffix and (file_suffix not in allow_suffix):
        return None, None, None
    file_content = ContentFile(file.read())
    if maxsize and file_content.size > maxsize:
        return None, None, None
    file_name = random_str(16) + file_suffix 
    while os.path.exists('../media/' + file_name):
        file_name = random_str(16) + file_suffix    #36^16种文件名，完全足够了QaQ，不会死循环
    return file_name, file_content, file_suffix

def random_str(random_length=6):
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

class ViewBase(View):
    def fail(self,msg=''):
        return JsonResponse({
            "result" : "fail",
            "msg" : msg
        })
    SUCCESS = JsonResponse({  "result" : "success"   })
    def get_usertype(self, request):
        if request.user.is_superuser:
            return 'root' if request.user.is_staff else 'admin'
        else:
            return 'guest'
