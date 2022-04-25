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