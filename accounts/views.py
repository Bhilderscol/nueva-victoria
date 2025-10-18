from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember = self.request.POST.get("remember_me") == "on"
        if remember:
            self.request.session.set_expiry(60 * 60 * 24 * 14)  # 14 dÃ­as
        else:
            self.request.session.set_expiry(0)  # expira al cerrar
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("dashboard")


class CustomLogoutView(LogoutView):
    next_page = "usuarios:login"

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

@require_GET
def logout_get(request):
    logout(request)
    return redirect("usuarios:login")