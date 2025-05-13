import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix_backend.settings')

app = Celery('videoflix_backend')

# Nimmt alle CELERY_* Settings aus settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Lädt alle tasks.py automatisch aus installierten Apps
app.autodiscover_tasks()
