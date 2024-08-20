from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()

# Configure le broker pour les messages de tâches (utilisez Redis ou un autre broker selon vos besoins)
app.conf.broker_url = 'redis://localhost:6379/0'


app.log.setup(loglevel='INFO', logfile= os.path.join(CORE_DIR, 'config/log/celery.log'))
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request:{self.request!r}')