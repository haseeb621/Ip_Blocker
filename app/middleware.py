from .models import *
from django.http import HttpResponseForbidden,HttpResponse
import geoip2
from Ip_Blocker import settings
import logging
from django.contrib.gis.geoip2 import GeoIP2

logger=logging.getLogger(__name__)


class IpMiddleWare:
 def __init__(self, get_response):
  self.get_response=get_response
  
 def __call__(self,request):
  # simulated_ip='8.8.8.8'
  # request.META['HTTP_X_FORWARDED_FOR']=simulated_ip
  user_ip=request.META.get('REMOTE_ADDR')
  forwarded_user_ip=request.META.get('HTTP_X_FORWARDED_FOR')
  ip=forwarded_user_ip.split(',')[0].strip() if forwarded_user_ip else user_ip
  if Block_List.objects.filter(ip_address=ip):
   return HttpResponseForbidden("Access Denied(Ip blocked)")

  return self.get_response(request)
 
class CountryIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip = GeoIP2(settings.GEOIP_PATH)

    def __call__(self, request):
        # Uncomment to test with a simulated IP
        simulated_ip = '8.8.8.8'
        request.META['HTTP_X_FORWARDED_FOR'] = simulated_ip
      
        user_ip = request.META.get('REMOTE_ADDR')
        forwarded_user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = forwarded_user_ip.split(',')[0].strip() if forwarded_user_ip else user_ip
        print(f"User IP: {ip}")

        try:
            country = self.geoip.country(ip)["country_code"]
            print(f"Country Code: {country}")
            if country in settings.BLOCKED_COUNTRIES:
                logger.info(f"Access denied for IP from blocked country: {ip}, Country: {country}")
                return HttpResponseForbidden("Access Denied (Country blocked)")
        except geoip2.errors.AddressNotFoundError:
            logger.warning(f"GeoIP lookup failed for IP: {ip}")
        except Exception as e:
            logger.error(f"Unexpected error in CountryIpMiddleware: {e}")

        return self.get_response(request)
