from datetime import timedelta
import environ
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
base = environ.Path(BASE_DIR)
environ.Env.read_env(env_file=base(".env"))


# Celery configurations
# For more information visit https://docs.celeryproject.org/en/v5.1.0/userguide/configuration.html


broker_url = os.environ["broker_url"]
# result_backend=os.environ["result_backend"]
# accept_content=os.environ["accept_content"]
# task_serializer=os.environ["task_serializer"]
# result_serializer=os.environ["result_serializer"]
timezone = os.environ["timezone"]
result_backend = "django-db"
cache_backend = "django-cache"
imports = ("dashboard.tasks",)
beat_schedule = {
    "sync-every-five-minutes": {
        "task": "dashboard.tasks.periodic_task",
        "schedule": timedelta(minutes=5.0),
    }
}
