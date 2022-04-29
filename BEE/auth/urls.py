from django.urls import path
from auth.views import LoginAPIVIEW, LogoutAPIView, AuthStatusAPIView



urlpatterns = [
    path("login", LoginAPIVIEW.as_view(), name="login"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("status", AuthStatusAPIView.as_view(), name="auth-status"),
]
