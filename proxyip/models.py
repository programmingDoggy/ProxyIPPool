from django.db import models
from django.utils.timezone import now
import requests,json


class ProxyIP(models.Model):
    ip = models.CharField(max_length=64)
    port = models.CharField(max_length=8)
    valid = models.BooleanField(default=True)
    create_time = models.DateTimeField(default=now)
    other = models.CharField(max_length=256)

    def __str__(self):
        return "{} IP: {} --- Port: {} --- Othre: {} === DateTime: {}".format(self.valid, self.ip, self.port, self.other, self.create_time)

    @classmethod
    def extract_ip(cls):
        url = "http://daili.spbeen.com/get_api_json/?token=68mHIdRjj7wLgsOxpECC9EHP&num=1"
        response = requests.get(url)
        try:
            info = json.loads(response.text)
        except:
            raise Exception("http server is down!")
        data = info.get('data', [])
        for proxyip in data:
            proxy_ip = proxyip['proxyip']
            ip, port = proxy_ip.split(':')
            backend_ip = proxyip['backend_ip']
            ProxyIP.objects.create(ip=ip, port=port, other=backend_ip)
        return True

    @classmethod
    def check_ip_valid(self, ipobj):
        url = "http://www.spbeen.com/tool/request_info/"
        proxys = {'http': 'http://{}{}'.format(ipobj.ip, ipobj.port), 'https': 'https://{}{}'.format(ipobj.ip, ipobj.port)}
        try:
            response = requests.get(url, proxys=proxys, timeout=3)
            if ipobj.other not in response.text:
                ipobj.valid = False
                ipobj.save()
        except:
            print("time out!!!")
            ipobj.valid = False
            ipobj.save()
