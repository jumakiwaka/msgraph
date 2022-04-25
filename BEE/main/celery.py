from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery("main")

app.config_from_object("main.celeryconfig", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
