from django.urls import path
from django.contrib.auth.views import LoginView
from .views import CustomLogoutView

app_name = "usuarios"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]