import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flights_project.settings')

app = Celery('flights_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 毎時 monitor_prices タスクを実行
app.conf.beat_schedule = {
    'monitor-prices-every-hour': {
        'task': 'monitor.tasks.monitor_prices',
        'schedule': crontab(minute=0),
    },
}
