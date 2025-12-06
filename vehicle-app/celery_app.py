from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "parking_app",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks"]       
)

celery.conf.timezone = "Asia/Kolkata"
celery.conf.enable_utc = False

from celery.schedules import crontab

REMINDER_TIME = int(os.getenv("REMINDER_TIME", 18))

celery.conf.beat_schedule = {
    "test-reminder-job": {
        "task": "tasks.send_daily_reminders",
        "schedule": 30.0,
    }
}

celery.conf.beat_schedule = {
    "monthly-report-job": {
        "task": "tasks.monthly_report_all",
        "schedule": crontab(
            minute=0,
            hour=6,
            day_of_month="1"
        ),  
    }
}

