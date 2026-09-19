# sistem/middleware/registro_visualizacao.py

from sistem.models import Acesso, Visualizacao

class RegistroVisualizacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # só registrar se estiver autenticado
        acesso_id = request.session.get('acesso_id')
        if acesso_id and not request.path.startswith('/admin') and request.user.is_authenticated:
            Visualizacao.objects.create(
                acesso_id=acesso_id,
                caminho=request.path
            )

        return response