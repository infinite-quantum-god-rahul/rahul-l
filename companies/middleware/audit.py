from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from companies.models import AuditLog
import json

class AuditLogMiddleware(MiddlewareMixin):
    def process_response(self, request: HttpRequest, response):
        try:
            user = getattr(request, "user", None)
            AuditLog.objects.create(
                user=user if getattr(user, "is_authenticated", False) else None,
                path=(request.path or "")[:255],
                method=(request.method or "")[:8],
                ip=(request.META.get("REMOTE_ADDR") or "")[:45],
                status=getattr(response, "status_code", 0),
                payload={
                    "GET": request.GET.dict(),
                    "POST": {k: ("<file>" if hasattr(v, "read") else v) for k, v in request.POST.items()},
                },
            )
        except Exception:
            pass
        return response
