from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("expediente", "nombre_completo", "fecha_ingreso", "tipo_adiccion")
    search_fields = ("expediente", "nombre_completo", "responsable_nombre")
    list_filter = ("fecha_ingreso", "tipo_adiccion")