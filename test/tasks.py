from celery import shared_task
from core.celery import app
from time import sleep
@shared_task(bind=True,default_retry_delay=5*60)
def add(self,x, y):
    try:
        return x + y
    except Exception as e:
        raise self.retry(exc=e, countdown=60)