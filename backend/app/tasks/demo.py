from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

@celery_app.task
def demo_task(project_id: int):
    print(f"[TASK] processing project {project_id}")
