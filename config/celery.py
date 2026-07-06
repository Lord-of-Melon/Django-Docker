import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

app = Celery("config")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()

app.conf.beat_schedule = {

    "update-course-statistics": {

        "task": "apps.tasks.statistics_tasks.update_course_statistics",

        "schedule": 60.0,
    },

    "export-course-report": {

        "task": "apps.tasks.report_tasks.export_course_report",

        "schedule": crontab(hour=0, minute=0),
    },
}