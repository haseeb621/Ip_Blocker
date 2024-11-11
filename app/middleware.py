from .models import *
from django.http import HttpResponseForbidden,HttpResponse

class IpMiddleWare():
 def __init__(self, get_response):
  self.get_response=get_response
  
 def __call__(self,request):
  user_ip=request.META.get('REMOTE_ADDR')
  forwarded_user_ip=request.META.get('HTTP_X_FORWARDED_FOR')
  print(user_ip)
  print(forwarded_user_ip)
  ip=forwarded_user_ip.split(',')[0].strip() if forwarded_user_ip else user_ip
  print(ip)
  if Block_List.objects.filter(ip_address=ip):
   return HttpResponseForbidden("Access Denied(Ip blocked)")

  return self.get_response(request)