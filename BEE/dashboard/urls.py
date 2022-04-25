from django.urls import path
from dashboard.views import index, connect, get_token, disconnect, logout, get_emails

urlpatterns = [
    path("", index, name="index"),
    path("connect", connect, name="connect"),
    path("getAToken", get_token, name="get_token"),
    path("disconnect", disconnect, name="disconnect"),
    path("logout", logout, name="logout"),
    path("task", get_emails, name="getEmails"),
]
