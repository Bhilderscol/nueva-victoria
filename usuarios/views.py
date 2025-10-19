# usuarios/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from .utils import user_in_groups


# ----------------------------------------------------------------------
# LOGOUT ROBUSTO
# ----------------------------------------------------------------------
def logout_view(request):
    """Cierra sesión (GET o POST) y redirige manejando el parámetro 
ext."""
    redirect_to = request.POST.get("next") or request.GET.get("next")
    if redirect_to and not url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        redirect_to = None

    messages.success(request, "Sesión cerrada correctamente.")
    logout(request)

    if redirect_to:
        return redirect(redirect_to)

    if getattr(settings, "LOGOUT_REDIRECT_URL", None):
        return redirect(settings.LOGOUT_REDIRECT_URL)

    return redirect(reverse("usuarios:login"))


# ----------------------------------------------------------------------
# CATÁLOGO DE CARDS POR ROL
# ----------------------------------------------------------------------
ALL_CARDS = [
    {
        "key": "pacientes",
        "title": "Pacientes",
        "desc": "Gestión integral de expedientes",
        "href": "/pacientes/",
        "icon": "bi-people",
        "groups": ["Director", "Lider"],
    },
    {
        "key": "contabilidad",
        "title": "Contabilidad",
        "desc": "Ingresos, egresos y reportes",
        "href": "/contabilidad/",
        "icon": "bi-cash-coin",
        "groups": ["Director", "Contador"],
    },
    {
        "key": "eventos",
        "title": "Eventos",
        "desc": "Programación de actividades",
        "href": "/eventos/",
        "icon": "bi-calendar-event",
        "groups": ["Director", "Organizador"],
    },
    {
        "key": "reportes",
        "title": "Reportes",
        "desc": "Indicadores y exportes",
        "href": "/reportes/",
        "icon": "bi-bar-chart",
        "groups": ["Director", "Responsable"],
    },
    {
        "key": "usuarios",
        "title": "Usuarios",
        "desc": "Gestión de personal y roles",
        "href": "/admin/auth/user/",
        "icon": "bi-person-gear",
        "groups": ["Director"],
    },
    {
        "key": "perfil",
        "title": "Mi Perfil",
        "desc": "Datos de cuenta",
        "href": "/accounts/profile/",
        "icon": "bi-person-circle",
        "groups": ["*"],
    },
    {
        "key": "ayuda",
        "title": "Ayuda",
        "desc": "Guías y soporte",
        "href": "/ayuda/",
        "icon": "bi-info-circle",
        "groups": ["*"],
    },
]


def visible_cards_for(user):
    """Filtra ALL_CARDS según los grupos del usuario."""
    if not user or not user.is_authenticated:
        return []
    if user.is_superuser:
        return ALL_CARDS
    visibles = []
    for c in ALL_CARDS:
        if "*" in c["groups"] or user_in_groups(user, c["groups"]):
            visibles.append(c)
    return visibles


# ----------------------------------------------------------------------
# DASHBOARD PRINCIPAL
# ----------------------------------------------------------------------
@login_required
def dashboard(request):
    cards = visible_cards_for(request.user)
    return render(request, "usuarios/dashboard.html", {"cards": cards})
