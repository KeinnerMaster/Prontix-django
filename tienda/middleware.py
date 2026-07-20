from django.shortcuts import render
from .models import ConfiguracionSitio


class MantenimientoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # No bloquear el panel de admin, para que siempre puedas entrar a desactivarlo
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        try:
            config = ConfiguracionSitio.objects.first()
        except Exception:
            config = None

        if config and config.modo_mantenimiento:
            # Si el visitante ya inició sesión como staff, lo dejamos pasar
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)

            return render(request, 'tienda/mantenimiento.html', {
                'mensaje': config.mensaje_mantenimiento
            }, status=503)

        return self.get_response(request)
