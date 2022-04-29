from django.urls import path
from dashboard.views import summary

urlpatterns = [
    path("summary", summary, name="summary"),
]
