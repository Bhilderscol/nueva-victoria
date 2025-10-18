from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("usuarios.urls")),   # login/logout
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),           # dashboard como home (/)
    path("pacientes/", include("pacientes.urls")), # ← NECESARIA
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
