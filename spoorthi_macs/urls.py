from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main-test/', lambda request: HttpResponse("MAIN TEST WORKS!"), name="main_test"),
    path('', include('companies.urls')),
    # Favicon
    re_path(r'^favicon\.ico$', serve, {'path': 'images/smlLogo1.ico', 'document_root': settings.STATIC_ROOT}),
]

# Media files (for photo uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
