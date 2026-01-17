from celery import Celery

app = Celery('tamarcado', broker= 'redis://localhost:6379/0') 


@app.task
def soma(a, b):
   return a + b