from django.shortcuts import render

from django.shortcuts import HttpResponse
import random
from proxyip.models import ProxyIP


def get_proxy_ip(request):
    proxy_ips = ProxyIP.objects.filter(valid=True)
    if proxy_ips.count() < 1:
        return HttpResponse("without available proxy ip")
    proxy_ip = random.choice(proxy_ips)
    return HttpResponse("{}:{}".format(proxy_ip.ip, proxy_ip.port))

