import time
from django.conf import settings

class HTMXLoadingMiddleware:
    """
    Adds a manual delay to HTMX requests during development
    so we can see loading indicators/spinners.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG and request.headers.get('HX-Request'):
            time.sleep(0.8)

        response = self.get_response(request)
        return response
