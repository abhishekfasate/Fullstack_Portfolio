"""Celery worker — async background tasks (GitHub sync, email)."""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

app = Celery("portfolio", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# ── Periodic tasks ────────────────────────────────────────────────────────────
app.conf.beat_schedule = {
    "sync-github-stars": {
        "task": "app.tasks.github_sync.sync_all_repos",
        "schedule": crontab(minute=0, hour="*/6"),   # every 6 hours
    },
}