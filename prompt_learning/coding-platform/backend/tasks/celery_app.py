"""
Celery configuration for async task processing
"""

from celery import Celery
import os

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://:redis_password@redis:6379/0")

# Initialize Celery
celery_app = Celery(
    "coding_platform",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['tasks'])

@celery_app.task(name="tasks.celery_app.test_task")
def test_task():
    """
    Test task for Celery
    """
    return "Celery is working!"
