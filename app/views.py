from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.
def index(request):
 return render(request,'index.html')
def check_ip(request):
 
 return HttpResponse('You are in the website')
 