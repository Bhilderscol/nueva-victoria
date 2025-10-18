from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nombre_completo","fecha_nacimiento","direccion","tipo_adiccion",
            "responsable_nombre","responsable_telefono","responsable_direccion",
            "fecha_ingreso","fecha_egreso_probable",
            "costo_semana","costo_laboratorios","costo_traslado",
            "foto_perfil",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "fecha_ingreso": forms.DateInput(attrs={"type": "date"}),
            "fecha_egreso_probable": forms.DateInput(attrs={"type": "date"}),
        }