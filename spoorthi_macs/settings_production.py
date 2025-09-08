import os
import dj_database_url
from pathlib import Path
from .settings import *

# Production settings for Render.com deployment

# Security settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-spoorthi-secret-key')

# Database configuration for Render.com
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Allowed hosts for production
ALLOWED_HOSTS = [
    'sml87-django-app.onrender.com',
    'localhost',
    '127.0.0.1',
]

# CSRF trusted origins for production
CSRF_TRUSTED_ORIGINS = [
    'https://sml87-django-app.onrender.com',
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8001',
    'https://localhost',
    'https://127.0.0.1',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
    'https://localhost:8001',
    'https://127.0.0.1:8001',
]

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (Render.com provides HTTPS)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
