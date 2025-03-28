from .signals import set_current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Armazena o usuário atual
        if hasattr(request, 'user'):
            set_current_user(request.user)

        response = self.get_response(request)
        return response
