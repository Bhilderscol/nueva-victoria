from django.urls import path
from .views import logout_get

urlpatterns = [
    path("logout/", logout_get, name="logout"),
]