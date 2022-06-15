from datetime import date, datetime
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from django.core.files.storage import default_storage
import os.path
from django.core.files.base import ContentFile
#from django.views.decorators.csrf import csrf_exempt
#from ..Ustc_Lost_And_Found import settings
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from common.common import *

class List(ViewBase):
    PAGE = 20
    def get(self, request):
        result = {
            "result" : "success", 
            "total_page" : 0,
            "privilege" : self.get_usertype(request),
            "data" : []
        }
        try:
            page = request.GET.get('page') or 1
            page = int(page)
        except Exception:
            return self.fail('页数格式不对')
        query = ReportPost.objects.filter().order_by('-time') #按照时间降序排列所有查询
        tot = (query.count() + page - 1) // page
        result['total_page'] = tot
        for i in range((page-1)*self.PAGE, min(page*self.PAGE,query.count())):
            rec = model_to_dict(query[i])  #rec表示一条记录。
            del rec['pic1'], rec['pic2'], rec['pic3'], rec['importace'] #这几项都不要
            rec['star_num'] = 0
            rec['is_star'] = 0
            result['data'].append(rec)
        return JsonResponse(result)

class Release(ViewBase):
    def post(self, request):
        try:
            para = {
                'author' : str(request.user.pk),
                'title' : request.POST.get('title'),
                'text' : request.POST.get('text'),
                'time' : datetime.now(),
                'importace': 0,  # 请注意，我不小心打错字母了。。。。。
                'reply' : ""
            }
            item = ReportPost(**para)
            '''
            for i in range(1, 4):
                name = f'pic{i}'
                file_name, file_content, _ = process_file(request.FILES.get(name))
                if not file_name:
                    continue
                getattr(item, name).save(file_name, file_content)
            '''
            item.save()
            return JsonResponse({
                "result" : "success", 
                "id" : item.id
            })
        except Exception as e:
            print(e)
            return self.fail('日期格式不对')

class Delete(ViewBase):
    def post(self, request):
        try:
            pk = int(request.POST.get('id'))
        except Exception:
            return self.fail('缺少必要参数id') 
        try:
            reply = ReportPost.objects.get(pk=pk)
        except Exception:
            return self.fail('找不到这个贴子')
        if self.get_usertype(request) == 'guest' and str(request.user.pk) != reply.author:
            return self.fail('权限不够')
        reply.delete()
        return self.SUCCESS

class Reply(ViewBase):
    def post(self, request):
        if self.get_usertype(request) == 'guest':
            return self.fail('权限不够')
        try:
            person = int(request.POST.get('id'))
            item = ReportPost.objects.get(pk=person)
        except Exception:
            return self.fail('格式不对')
        txt = request.POST.get('text')
        if not txt:
            return self.fail('你没有添加评论')
        item.reply = txt
        item.reply_time = datetime.now()
        item.save()
        return self.SUCCESS

class Star(ViewBase):
    pass