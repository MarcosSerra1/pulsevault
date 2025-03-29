from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import MiddlewareNotUsed
from contextvars import ContextVar

# Contexto global para o usuário atual
CURRENT_USER = ContextVar('current_user', default=None)


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware para gerenciar o usuário atual de forma thread-safe.

    Usa contextvars para garantir isolamento entre requisições.
    """
    def process_request(self, request):
        """Armazena o usuário atual no contexto"""
        if hasattr(request, 'user'):
            CURRENT_USER.set(request.user)

    def process_response(self, request, response):
        """Limpa o contexto após a resposta"""
        try:
            CURRENT_USER.set(None)
        except LookupError:
            pass
        return response
