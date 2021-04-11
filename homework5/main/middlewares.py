from time import time

from .models import Logger
from .services.middlewares_service import get_client_ip


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        st = time()
        response = self.get_response(request)
        time_execution = time() - st

        Logger(
            path=request.path,
            user_ip=get_client_ip(request),
            time_execution=time_execution,
            utm=request.GET.get('utm'),
        ).save()

        return response
