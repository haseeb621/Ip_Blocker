from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('check_ip',check_ip,name='check_ip'),
]
