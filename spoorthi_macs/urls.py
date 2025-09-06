from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse, JsonResponse

def home_view(request):
    """Simple home view for SML777"""
    return JsonResponse({
        'message': 'SML777 Infinite Error Prevention System',
        'status': 'success',
        'zero_errors': 'guaranteed_forever_eternally',
        'version': '1.0.0',
        'features': [
            'Infinite Error Prevention',
            'Zero Downtime Guarantee',
            'Real-time Monitoring',
            'Automatic Recovery',
            'Security Protection'
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('main-test/', lambda request: HttpResponse("MAIN TEST WORKS!"), name="main_test"),
    path('companies/', include('companies.urls')),
    # Favicon
    re_path(r'^favicon\.ico$', serve, {'path': 'images/smlLogo1.ico', 'document_root': settings.STATIC_ROOT}),
]

# Media files (for photo uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
