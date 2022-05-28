from datetime import date, datetime
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from django.core.files.storage import default_storage
#from django.views.decorators.csrf import csrf_exempt
#from ..Ustc_Lost_And_Found import settings

# Create your views here.
class ViewBase(View):
    def fail(self,msg=''):
        return JsonResponse({
            "result" : "fail",
            "msg" : msg
        })
    SUCCESS = JsonResponse({  "result" : "success"   })


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
        if request.GET.get('title'):
            para['title__contains'] = request.GET.get('title')
        if request.GET.get('date_old'):
            try:
                para['date__gte'] = date.fromisoformat(request.GET.get('date_old'))
            except ValueError:
                return self.fail('日期格式不对')
        if request.GET.get('date_new'):
            try:
                para['date__lte'] = date.fromisoformat(request.GET.get('date_new'))
            except ValueError:
                return self.fail('日期格式不对')
        if request.GET.get('place'):
            para['place'] = request.GET.get('place')
        if request.GET.get('name'):
            para['name'] = request.GET.get('name')
        para['type'] = request.GET.get('type') or 'F'
        try:
            page = request.GET.get('page') or 1
            page = int(page)
        except Exception:
            return self.fail('页数格式不对')
        query = LFPost.objects.filter(**para).order_by('-time') #按照时间降序排列所有查询
        tot = (query.count() + page - 1) // page
        result['total_page'] = tot
        for i in range((page-1)*self.PAGE, min(page*self.PAGE,query.count())):
            rec = model_to_dict(query[i])  #rec表示一条记录。
            del rec['pic1'], rec['pic2'], rec['pic3'], rec['text']  #这几项都不要
            result['data'].append(rec)
        return JsonResponse(result)


class Release(ViewBase):
    def post(self, request):
        print('-'*20)
        print(request.POST.get('date'))
        print(request.POST.get('title'))
        print('-'*20)
        try:
            para = {
                'author' : 'root', #这个地方，应该用鉴权模块自动配置，这里初始阶段先暂时跳过，此后再修补
                'date' : date.fromisoformat(request.POST.get('date')),  #如果这个地方有异常直接就fail了
                'place' : request.POST.get('place'),
                'name' : request.POST.get('name'),
                'title' : request.POST.get('title'),
                'text' : request.POST.get('text'),
                'public' : request.POST.get('public'),
                'time' : datetime.now(),
                'status' : 0,
                'type' : request.POST.get('type')
            }
            if para['type'] != 'L' and para['type'] != 'F':
                return self.fail('type格式不对')
            if para['public'] == '0':
                para['public'] = False
            elif para['public'] == '1':
                para['public'] = True
            else:
                return self.fail('public格式不对')
            if not (para['place'] and para['title'] and para['name']):
                return self.fail('缺少必要参数')    #这三个字段不让为空
            para['pic1'] = request.FILES.get('pic1') or ''
            para['pic2'] = request.FILES.get('pic2') or ''
            para['pic3'] = request.FILES.get('pic3') or ''
            item = LFPost(**para)
            item.save()
            return JsonResponse({
                "result" : "success", 
                "id" : item.id
            })
        except Exception:
            return self.fail('日期格式不对')

class Delete(ViewBase):
    def post(self, request):
        try:
            pk = int(request.POST.get('id'))
            if LFPost.objects.filter(pk=pk).delete()[0] == 0:
                return self.fail('找不到这个帖子')
            return self.SUCCESS
        except Exception:
            return self.fail('缺少必要参数id')
        

class Pick(ViewBase):
    def post(self, request):
        try:
            pk = int(request.POST.get('id'))
            rec = LFPost.objects.filter(pk=pk)[0]
            if rec.status == 0:
                rec.status = 1
                rec.save()
            else:
                return self.fail('该操作已经被进行了')
            return self.SUCCESS
        except Exception:
            return self.fail('缺少必要参数id或格式不对')

class Confirm(ViewBase):
    def post(self, request):
        try:
            pk = int(request.POST.get('id'))
            rec = LFPost.objects.filter(pk=pk)[0]
            if rec.status == 1:
                rec.status = 2
                rec.save()
            else:
                return self.fail('该操作已经被进行了')
            return self.SUCCESS
        except Exception:
            return self.fail('缺少必要参数id或格式不对')


class Reply(ViewBase):
    def post(self, request):
        try:
            para = {
                'author' : 'root', #这个地方，应该用鉴权模块自动配置，这里初始阶段先暂时跳过，此后再修补
                'post_id' : int(request.POST.get('post_id')),
                'text' : request.POST.get('text'),
                'public' : request.POST.get('public'),
                'time' : datetime.now()
            }
            if para['public'] == '0':
                para['public'] = False
            elif para['public'] == '1':
                para['public'] = True
            else:
                return self.fail('public格式不对')
            para['pic1'] = request.FILES.get('pic1') or ''
            para['pic2'] = request.FILES.get('pic2') or ''
            para['pic3'] = request.FILES.get('pic3') or ''
            LFReply(**para).save()
        except Exception:
            return self.fail('缺少必要参数id或格式不对')

class LfQuery(ViewBase):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return self.fail('您未登录')
        return render(request, 'lf.html')