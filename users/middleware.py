import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class UserAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            logger.info(
                'Ação do usuário: %s, Path: %s, Method: %s, Time: %s',
                request.user.email,
                request.path,
                request.method,
                timezone.now()
            )

        return response
