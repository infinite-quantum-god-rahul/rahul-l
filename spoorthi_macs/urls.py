from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('companies.urls')),
    # REST API for mobile app (JWT + upload + lists)
    path('api/', include('companies.api_urls')),
    # Favicon
    re_path(r'^favicon\.ico$', serve, {'path': 'images/smlLogo1.ico', 'document_root': settings.STATIC_ROOT}),
]

# Media files (for photo uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
