import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamarcado.settings.base')


app = Celery('tamarcado') 
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task
def soma(a, b):
   return a + b
