import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_service_api.settings")

app = Celery("library_service_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "notify-borrowings-daily": {
        "task": "tasks.tasks.notify_borrowings_deadlines",
        "schedule": crontab(hour=8, minute=0),
    },
}