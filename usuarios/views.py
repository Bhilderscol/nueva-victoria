# --- logout simple por GET, robusto ---
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """
    Cierra sesión (GET o POST) y redirige al login con mensaje.
    """
    logout(request)
    from django.contrib import messages
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("usuarios:login")
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse
def user_in_group(user, group_name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

@login_required
def dashboard(request):
    is_director = user_in_group(request.user, "Director") or request.user.is_superuser
    is_lider = user_in_group(request.user, "Lider")
    is_conta = user_in_group(request.user, "Contabilidad")

    cards = []
    if is_director:
        cards.extend([
            {"title": "Pacientes", "desc": "Gestion integral de pacientes", "href": "/pacientes/"},
            {"title": "Contabilidad", "desc": "Ingresos, egresos y reportes", "href": "/contabilidad/"},
            {"title": "Reportes", "desc": "Indicadores y exportaciones", "href": "/reportes/"},
            {"title": "Usuarios", "desc": "Administracion de personal y roles", "href": "/admin/auth/user/"},
        ])
    else:
        if is_lider:
            cards.append({"title": "Pacientes", "desc": "Gestion de expedientes", "href": "/pacientes/"})
        if is_conta:
            cards.append({"title": "Contabilidad", "desc": "Movimientos y balances", "href": "/contabilidad/"})

    cards.extend([
        {"title": "Mi Perfil", "desc": "Datos de cuenta", "href": "/accounts/profile/"},
        {"title": "Ayuda", "desc": "Guias y soporte", "href": "/ayuda/"},
    ])

    context = {"cards": cards, "is_director": is_director, "is_lider": is_lider, "is_conta": is_conta}
    template_path = "usuarios/dashboard.html"
    return render(request, template_path, context)

@login_required
def pacientes_home(request):
    return HttpResponse("<h1>Pacientes</h1><p>Modulo en construccion.</p>")
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("usuarios:login")

    def post(self, request, *args, **kwargs):
        messages.success(request, "Sesion cerrada correctamente.")
        return super().post(request, *args, **kwargs)