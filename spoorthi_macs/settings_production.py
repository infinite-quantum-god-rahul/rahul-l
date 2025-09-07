"""
SML777 - Production Django Settings for Render Deployment
========================================================

This is a production-ready Django settings file optimized for Render.com deployment.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Render.com specific ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    '*.onrender.com',
]

# Add your custom domain here if you have one
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  # For static files on Render
    'companies',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spoorthi_macs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                "companies.context_processors.user_header_info",
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spoorthi_macs.wsgi.application'

# Database Configuration for Render
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Cache configuration for Render
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'sml777-cache',
    }
}

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation (relaxed for development)
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Date/Time formats
from django.conf.locale.en import formats as en_formats
en_formats.DATE_INPUT_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]
en_formats.DATETIME_INPUT_FORMATS = ["%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "companies/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise configuration for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Session configuration
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 14 * 24 * 3600  # 2 weeks

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# SML Feature Flags
SML_FEATURES = {
    "CREDIT_BUREAU": True,
    "NPA_DASHBOARD": True,
    "OFFLINE_KYC": True,
    "ESCALATION_ALERTS": True,
    "SMS": True,
    "PAYMENTS": True,
    "BORROWER_PORTAL": True,
}

# Credit Bureau Configuration
SML_CREDIT_BUREAU = {
    "PROVIDER": os.getenv("SML_BUREAU_PROVIDER", "CIBIL").upper(),
    "CIBIL": {
        "BASE_URL": os.getenv("CIBIL_BASE_URL", ""),
        "API_KEY": os.getenv("CIBIL_API_KEY", ""),
    },
    "CRIF": {
        "BASE_URL": os.getenv("CRIF_BASE_URL", ""),
        "API_KEY": os.getenv("CRIF_API_KEY", ""),
    },
}

# Payment Configuration
SML_PAYMENT = {
    "PROVIDER": os.getenv("RAZORPAY_PROVIDER", "RAZORPAY"),
    "KEY_ID": os.getenv("RAZORPAY_KEY_ID", ""),
    "KEY_SECRET": os.getenv("RAZORPAY_KEY_SECRET", ""),
}

# Alert Channels
SML_ALERT_CHANNELS = {
    "EMAIL": {"ENABLED": False, "FROM": os.getenv("ALERT_FROM_EMAIL", ""), "SMTP_URL": os.getenv("ALERT_SMTP_URL", "")},
    "SMS": {"ENABLED": False, "GATEWAY_URL": os.getenv("ALERT_SMS_URL", ""), "API_KEY": os.getenv("ALERT_SMS_KEY", "")},
    "WEBHOOK": {"ENABLED": False, "URL": os.getenv("ALERT_WEBHOOK_URL", "")},
}

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Production Security Settings
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Additional security headers
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

# Append slash
APPEND_SLASH = True

# Error prevention settings (from your original config)
ERROR_PREVENTION_ENABLED = True
ERROR_PREVENTION_LOG_LEVEL = 'INFO'
ERROR_PREVENTION_ALERT_EMAIL = os.getenv('ADMIN_EMAIL')

# Rate limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS_PER_MINUTE = 100
RATE_LIMIT_BURST_SIZE = 200

# Health check
HEALTH_CHECK_ENABLED = True
HEALTH_CHECK_INTERVAL = 30
HEALTH_CHECK_TIMEOUT = 10

# Monitoring
MONITORING_ENABLED = True
MONITORING_METRICS_RETENTION = 86400
MONITORING_ALERT_THRESHOLD = 5

# Backup settings
BACKUP_ENABLED = True
BACKUP_INTERVAL = 86400
BACKUP_RETENTION_DAYS = 30

# Security settings
SECURITY_HEADERS_ENABLED = True
SECURITY_RATE_LIMITING_ENABLED = True
SECURITY_SUSPICIOUS_PATTERN_DETECTION = True

# Performance settings
PERFORMANCE_MONITORING_ENABLED = True
PERFORMANCE_OPTIMIZATION_ENABLED = True
PERFORMANCE_CACHE_OPTIMIZATION = True

# Database error prevention
DATABASE_ERROR_PREVENTION_ENABLED = True
DATABASE_CONNECTION_POOLING = True
DATABASE_QUERY_OPTIMIZATION = True
DATABASE_BACKUP_ON_ERROR = True

# API error prevention
API_ERROR_PREVENTION_ENABLED = True
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 1
API_TIMEOUT = 30

# Frontend error prevention
FRONTEND_ERROR_PREVENTION_ENABLED = True
FRONTEND_CACHE_OPTIMIZATION = True
FRONTEND_RESOURCE_OPTIMIZATION = True

# Mobile app error prevention
MOBILE_APP_ERROR_PREVENTION_ENABLED = True
MOBILE_APP_UPDATE_CHECK = True
MOBILE_APP_CRASH_REPORTING = True

# Deployment error prevention
DEPLOYMENT_ERROR_PREVENTION_ENABLED = True
DEPLOYMENT_ROLLBACK_ENABLED = True
DEPLOYMENT_HEALTH_CHECK = True
