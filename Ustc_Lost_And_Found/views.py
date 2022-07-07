from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def mainpage(request):
    return render(request, 'lf.html')

@login_required
def lf_release(request):
    return render(request, 'lf_release.html')

@login_required
def report(request):
    return render(request, 'report.html')

@login_required
def tips(request):
    return render(request, 'tips.html')

@login_required
def qa(request):
    return render(request, 'qa.html')

@login_required
def user(request):
    return render(request, 'user.html')    

def register(request):
    return render(request, 'register.html')

def forget(request):
    return render(request, 'forget.html')

@login_required
def qa_release(request):
    return render(request, 'qa_release.html')

@login_required
def report_release(request):
    return render(request, 'report_release.html')

from au.views import UserQuery
import json

user_query = UserQuery()
@login_required
def show_user(request, pk):
    return render(request, 'new_user.html', json.loads(user_query.get(request, pk).content))
