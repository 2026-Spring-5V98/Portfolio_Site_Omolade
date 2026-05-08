from .models import SiteVisit


class VisitTrackerMiddleware:
    SKIP = ('/admin', '/static', '/media', '/chatbot', '/favicon', '/dashboard')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'GET' and not any(request.path.startswith(p) for p in self.SKIP):
            try:
                SiteVisit.objects.create(
                    path=request.path,
                    ip_address=self._get_ip(request),
                )
            except Exception:
                pass
        return response

    def _get_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
