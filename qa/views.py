from datetime import date, datetime
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from django.core.files.storage import default_storage
import os.path
import sys
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from common.common import *

class List(ViewBase):
    PAGE = 20
    def get(self, request):
        result = {
            "result" : "success", 
            "total_page" : 0,
            "privilege" : "root",   #之后修补
            "data" : []
        }
        para = {}
        page = request.GET.get('page') or 1
        try:
            page = int(page)
        except Exception:
            return self.fail('输入数据不合法')
        para['type'] = request.GET.get('type') or 'Q'
        query = Qa.objects.filter(**para).order_by('-top','-time') #按照时间降序排列所有查询
        tot = (query.count() + page - 1) // page
        result['total_page'] = tot
        for i in range((page-1)*self.PAGE, min(page*self.PAGE,query.count())):
            rec = model_to_dict(query[i])  #rec表示一条记录。
            rec['top'] = int(rec['top'])
            result['data'].append(rec)  
        return JsonResponse(result)


class Release(ViewBase):
    def post(self, request):
        try:
            para = {
                'q' : request.POST.get('q'),
                'a' : request.POST.get('a'),
                'top' : bool(request.POST.get('top')),
                'time' : datetime.now(),
                'type' : request.POST.get('type')
            }
            if not (para['q'] and para['a']):
                return self.fail('缺少必要参数')    #这三个字段不让为空
            if para['type'] not in ['Q', 'T']:
                return self.fali('type的格式不对！')
            item = Qa(**para)
            item.save()
            return JsonResponse({
                "result" : "success", 
                "id" : item.id
            })
        except Exception:
            return self.fail('格式不对')

class Delete(ViewBase):
    def post(self, request):
        try:
            pk = int(request.POST.get('id'))
            if Qa.objects.filter(pk=pk).delete()[0] == 0:
                return self.fail('找不到这个帖子')
            return self.SUCCESS
        except Exception:
            return self.fail('缺少必要参数id')

class Change(ViewBase):
    def post(self, request):
        try:
            pk = int(request.POST.get('id'))
            rec = Qa.objects.filter(pk=pk)[0]
            if request.POST.get('q'):
                rec.q = request.POST.get('q')
            if request.POST.get('a'):
                rec.a = request.POST.get('a')
            if request.POST.get('top'):
                rec.top = bool(request.POST.get('top'))            
            rec.save()
            return self.SUCCESS
        except Exception:
            return self.fail('缺少必要参数id或格式不对')


class QaQuery(ViewBase):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return self.fail('您未登录')
        return render(request, 'qa.html')