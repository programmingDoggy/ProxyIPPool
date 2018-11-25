import random
import time

from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from proxyip.models import ProxyIP
from concurrent import futures

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=5, replace_existing=True)
def extract_ip():
    ProxyIP.extract_ip()


@register_job(scheduler, "interval", seconds=25, replace_existing=True)
def check_ip_is_valid(): # 并发检测
    proxy_ips = ProxyIP.objects.filter(valid=True)
    num = ProxyIP.objects.filter(valid=True).count()
    if num > 10:
        num = 10
    if num < 1:
        print("no available proxy ip.")
    else:
        with futures.ThreadPoolExecutor(num) as executer:
            executer.map(ProxyIP.check_ip_valid, proxy_ips)

register_events(scheduler)
scheduler.start()
