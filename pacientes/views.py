from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Paciente
from .forms import PacienteForm

def is_lider(user):
    return user.is_authenticated and user.groups.filter(name="Lider").exists()

def is_director_organizador(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__in=["Director", "Organizador"]).exists())

class PacienteListaView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "pacientes/lista.html"
    context_object_name = "pacientes"
    paginate_by = 20

class PacienteCrearView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pacientes/form.html"
    success_url = reverse_lazy("pacientes_lista")
    def test_func(self):
        # Lider puede crear; Director/Organizador tambien
        return is_lider(self.request.user) or is_director_organizador(self.request.user)

class PacienteDetalleView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = "pacientes/detalle.html"
    context_object_name = "paciente"