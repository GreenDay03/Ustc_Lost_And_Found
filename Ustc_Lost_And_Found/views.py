from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')