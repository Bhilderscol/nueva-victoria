from django.urls import path
from .views import PacienteListaView, PacienteCrearView, PacienteDetalleView

urlpatterns = [
    path("", PacienteListaView.as_view(), name="pacientes_lista"),
    path("nuevo/", PacienteCrearView.as_view(), name="pacientes_nuevo"),
    path("<int:pk>/", PacienteDetalleView.as_view(), name="pacientes_detalle"),
]