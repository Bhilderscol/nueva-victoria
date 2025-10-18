# fix_dashboard.ps1
$ErrorActionPreference = "Stop"

function Ensure-Dir($p){ if(-not(Test-Path $p)){ New-Item -Type Directory -Force -Path $p | Out-Null } }
function Read-AllText($p){ if(Test-Path $p){ return [IO.File]::ReadAllText($p) } else { return "" } }
function Write-UTF8($p,$t){ Ensure-Dir ([IO.Path]::GetDirectoryName($p)); [IO.File]::WriteAllText($p,[string]$t,(New-Object System.Text.UTF8Encoding($false))) }

# 0) Verificaciones básicas
$proj = (Get-Location).Path
$manage = Join-Path $proj "manage.py"
if(-not (Test-Path $manage)){ throw "Ejecuta este script desde la carpeta del proyecto (donde está manage.py)." }

# Detectar settings/urls del proyecto
$settings = Join-Path $proj "config\settings.py"
if(-not(Test-Path $settings)){ $settings = Join-Path $proj "config\config\settings.py" }
$projUrls = Join-Path $proj "config\urls.py"
if(-not(Test-Path $projUrls)){ $projUrls = Join-Path $proj "config\config\urls.py" }
if(-not(Test-Path $settings)){ throw "No encuentro config\settings.py" }
if(-not(Test-Path $projUrls)){ throw "No encuentro config\urls.py" }

# 1) Crear app dashboard si falta
$dashDir = Join-Path $proj "dashboard"
if(-not(Test-Path $dashDir)){
  & python manage.py startapp dashboard
  Write-Host "✔ App 'dashboard' creada"
} else {
  Write-Host "✔ App 'dashboard' ya existe"
}

# 2) Crear/asegurar archivos mínimos de dashboard
$dashUrlsPath = Join-Path $dashDir "urls.py"
$dashViewsPath = Join-Path $dashDir "views.py"

$dashUrls = @'
from django.urls import path
from .views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]
'@
Write-UTF8 $dashUrlsPath $dashUrls

$dashViews = @'
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
'@
Write-UTF8 $dashViewsPath $dashViews

# 3) Template del dashboard
$tplRoot = Join-Path $proj "templates"
$tplDash = Join-Path $tplRoot "dashboard"
Ensure-Dir $tplDash
$dashTpl = Join-Path $tplDash "index.html"
$dashHtml = @'
{% extends "base.html" %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<div class="container py-4">
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h4 class="mb-0">Dashboard</h4>
    <a class="btn btn-outline-secondary btn-sm" href="/accounts/logout/">Cerrar sesión</a>
  </div>
  <div class="alert alert-info">Dashboard cargado correctamente. Ahora puedes añadir las tarjetas por rol.</div>
</div>
{% endblock %}
'@
Write-UTF8 $dashTpl $dashHtml

# base.html (solo si no existe)
$baseTpl = Join-Path $tplRoot "base.html"
if(-not(Test-Path $baseTpl)){
$baseHtml = @'
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{% block title %}Nueva Victoria{% endblock %}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  {% block content %}{% endblock %}
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'@
  Write-UTF8 $baseTpl $baseHtml
  Write-Host "✔ templates/base.html creado"
} else {
  Write-Host "✔ templates/base.html existente"
}

# 4) Agregar "dashboard" a INSTALLED_APPS y asegurar TEMPLATES.DIRS + LOGIN redirects
$stxt = Read-AllText $settings

if($stxt -notmatch '"dashboard"'){
  $stxt = [regex]::Replace($stxt, '(INSTALLED_APPS\s*=\s*\[)', '$1' + "`r`n    ""dashboard"",", "Singleline")
  Write-Host '✔ Agregado "dashboard" a INSTALLED_APPS'
}

if($stxt -notmatch 'TEMPLATES\[0\]\["DIRS"\]\.append\(BASE_DIR / "templates"\)'){
$appendTpl = @'
# Asegurar carpeta templates
try:
    if (BASE_DIR / "templates") not in TEMPLATES[0]["DIRS"]:
        TEMPLATES[0]["DIRS"].append(BASE_DIR / "templates")
except Exception:
    pass
'@
  $stxt += "`r`n" + $appendTpl + "`r`n"
  Write-Host "✔ Asegurado BASE_DIR/templates en TEMPLATES.DIRS"
}

if($stxt -notmatch 'LOGIN_REDIRECT_URL'){
$appendAuth = @'
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
'@
  $stxt += "`r`n" + $appendAuth + "`r`n"
  Write-Host "✔ Configuradas LOGIN/LOGOUT redirects"
}

Write-UTF8 $settings $stxt

# 5) Incluir dashboard en urls del proyecto (home "/")
$projUrlsTxt = Read-AllText $projUrls
if($projUrlsTxt -notmatch 'include\("dashboard.urls"\)'){
  # Reescribir urls.py de forma segura y simple
$projUrlsNew = @'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("usuarios.urls")),
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),           # dashboard como home
    path("pacientes/", include("pacientes.urls")), # si ya tienes la app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'@
  Write-UTF8 $projUrls $projUrlsNew
  Write-Host "✔ config/urls.py actualizado (dashboard en /)"
} else {
  Write-Host "✔ config/urls.py ya incluye dashboard"
}

Write-Host ""
Write-Host "Todo listo. Pasos:" -ForegroundColor Yellow
Write-Host "1) Activa venv y arranca: .\venv\Scripts\activate ; python manage.py runserver"
Write-Host "2) Entra a: http://127.0.0.1:8000/accounts/login/  (tras login te manda a /)"
Write-Host "3) Si aún falla, pega el contenido de config/urls.py y la lista de apps en settings.py"
