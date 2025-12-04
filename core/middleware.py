import re

from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Require authentication for all requests except those whose path matches
    a regex in `settings.LOGIN_EXEMPT_URLS` or the configured `LOGIN_URL`.

    Add this middleware after `AuthenticationMiddleware` so `request.user`
    is available.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        exempt = getattr(settings, 'LOGIN_EXEMPT_URLS', [])
        # Ensure the login URL itself is exempt
        login_url = settings.LOGIN_URL.lstrip('/') if settings.LOGIN_URL else ''
        if login_url:
            # allow prefix match for the login URL
            exempt = list(exempt) + [r'^' + re.escape(login_url)]

        self.exempt_urls = [re.compile(expr) for expr in exempt]

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            if not any(pattern.match(path) for pattern in self.exempt_urls):
                # Redirect to login page, preserving next
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)
