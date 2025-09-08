"""
SML777 - Minimal Django Settings for Deployment
==============================================

This is a minimal Django settings file that will work on Render.com
without any complex dependencies or configurations.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-spoorthi-secret-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Allow Render.com domains and localhost for development
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    '.onrender.com',
    '*.onrender.com',
    'sml777.onrender.com',  # Your specific Render domain
]

# HTTPS Settings
SECURE_SSL_REDIRECT = False  # Disabled for development
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 0  # Disabled for development
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',  # For HTTPS support
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
                'django.template.context_processors.request',  # needed for role-based UI in templates
                'django.contrib.auth.context_processors.auth',  # must come before user_header_info
                # "companies.context_processors.user_header_info",  # Temporarily disabled due to database issue
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spoorthi_macs.wsgi.application'

# --- Database Configuration ---
# Use PostgreSQL on Render, SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Try to use PostgreSQL if DATABASE_URL is available
if os.getenv('DATABASE_URL'):
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
        }
    except ImportError:
        # Fallback to SQLite if dj_database_url is not available
        pass
#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': DB_NAME,
        #'USER': DB_USER,
        #'PASSWORD': DB_PASSWORD,
        #'HOST': DB_HOST,
        #'PORT': DB_PORT,
        #'CONN_MAX_AGE': 60,  # keep-alive in dev; safe
        #'OPTIONS': {
            #'charset': 'utf8mb4',
            #'connect_timeout': 10,
            #"init_command": "SET SESSION sql_mode='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ZERO_DATE,NO_ZERO_IN_DATE'",
        #},
    #}
#}

# --- Cache for login throttling/OTP step-up (used in views.login_view) ---
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'sml8-login-throttle',
    }
}

# Keep Django’s default backend so Groups/Permissions work with the users
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = []  # keep as-is for dev; add validators in prod

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Align server with dd/mm/yyyy inputs used in modals/Flatpickr
from django.conf.locale.en import formats as en_formats  # noqa: E402
en_formats.DATE_INPUT_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]
en_formats.DATETIME_INPUT_FORMATS = ["%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "companies/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # harmless in dev; useful for collectstatic later

# WhiteNoise configuration for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Session/Cookie hardening (works in dev; stricter in prod below) ---
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
# Default session age (two weeks); "remember me" in view can override per-session
SESSION_COOKIE_AGE = 14 * 24 * 3600

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# INFINITE ERROR PREVENTION CONFIGURATION
# ========================================

# Redis configuration for error prevention monitoring
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Sentry configuration for error tracking
SENTRY_DSN = None  # Set your Sentry DSN here for production

# Error prevention settings
ERROR_PREVENTION_ENABLED = True
ERROR_PREVENTION_LOG_LEVEL = 'INFO'
ERROR_PREVENTION_ALERT_EMAIL = None  # Set admin email for alerts

# Rate limiting settings
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS_PER_MINUTE = 100
RATE_LIMIT_BURST_SIZE = 200

# Health check settings
HEALTH_CHECK_ENABLED = True
HEALTH_CHECK_INTERVAL = 30  # seconds
HEALTH_CHECK_TIMEOUT = 10  # seconds

# Monitoring settings
MONITORING_ENABLED = True
MONITORING_METRICS_RETENTION = 86400  # 24 hours in seconds
MONITORING_ALERT_THRESHOLD = 5  # errors per minute

# Backup settings
BACKUP_ENABLED = True
BACKUP_INTERVAL = 86400  # 24 hours in seconds
BACKUP_RETENTION_DAYS = 30

# Security settings
SECURITY_HEADERS_ENABLED = True
SECURITY_RATE_LIMITING_ENABLED = True
SECURITY_SUSPICIOUS_PATTERN_DETECTION = True

# Performance settings
PERFORMANCE_MONITORING_ENABLED = True
PERFORMANCE_OPTIMIZATION_ENABLED = True
PERFORMANCE_CACHE_OPTIMIZATION = True

# Database error prevention settings
DATABASE_ERROR_PREVENTION_ENABLED = True
DATABASE_CONNECTION_POOLING = True
DATABASE_QUERY_OPTIMIZATION = True
DATABASE_BACKUP_ON_ERROR = True

# API error prevention settings
API_ERROR_PREVENTION_ENABLED = True
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 1  # seconds
API_TIMEOUT = 30  # seconds

# Frontend error prevention settings
FRONTEND_ERROR_PREVENTION_ENABLED = True
FRONTEND_CACHE_OPTIMIZATION = True
FRONTEND_RESOURCE_OPTIMIZATION = True

# Mobile app error prevention settings
MOBILE_APP_ERROR_PREVENTION_ENABLED = True
MOBILE_APP_UPDATE_CHECK = True
MOBILE_APP_CRASH_REPORTING = True

# Deployment error prevention settings
DEPLOYMENT_ERROR_PREVENTION_ENABLED = True
DEPLOYMENT_ROLLBACK_ENABLED = True
DEPLOYMENT_HEALTH_CHECK = True

# ────────────────────────────────────────────────────────────────────
# SML FEATURE FLAGS & PROVIDERS (SAFE DEFAULTS; PRESERVES EXISTING LOGIC)
# ────────────────────────────────────────────────────────────────────
SML_FEATURES = {
    "CREDIT_BUREAU": True,      # enable API stubs/endpoints for credit score pulls
    "NPA_DASHBOARD": True,      # enable NPA dashboard route/template
    "OFFLINE_KYC": True,        # enable KYCDocument entity (modal/grid)
    "ESCALATION_ALERTS": True,  # enable alert rules + management command
}
# Extend with new modules (borrower OTP, payments, SMS)
SML_FEATURES.update({
    "SMS": True,
    "PAYMENTS": True,
    "BORROWER_PORTAL": True,
})

SML_CREDIT_BUREAU = {
    "PROVIDER": os.getenv("SML_BUREAU_PROVIDER", "CIBIL").upper(),  # or "CRIF"
    "CIBIL": {
        "BASE_URL": os.getenv("CIBIL_BASE_URL", ""),
        "API_KEY":  os.getenv("CIBIL_API_KEY", ""),
    },
    "CRIF": {
        "BASE_URL": os.getenv("CRIF_BASE_URL", ""),
        "API_KEY":  os.getenv("CRIF_API_KEY", ""),
    },
}

# Payment provider config (used by companies.services.payments)
SML_PAYMENT = {
    "PROVIDER": os.getenv("RAZORPAY_PROVIDER", "RAZORPAY"),
    "KEY_ID": os.getenv("RAZORPAY_KEY_ID", ""),
    "KEY_SECRET": os.getenv("RAZORPAY_KEY_SECRET", ""),
}

SML_ALERT_CHANNELS = {
    "EMAIL":   {"ENABLED": False, "FROM": os.getenv("ALERT_FROM_EMAIL", ""), "SMTP_URL": os.getenv("ALERT_SMTP_URL", "")},
    "SMS":     {"ENABLED": False, "GATEWAY_URL": os.getenv("ALERT_SMS_URL", ""), "API_KEY": os.getenv("ALERT_SMS_KEY", "")},
    "WEBHOOK": {"ENABLED": False, "URL": os.getenv("ALERT_WEBHOOK_URL", "")},
}

# Minimal console logging; pairs with AuditLogMiddleware without file IO
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django.db.backends': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False},
    },
}



# --- Production-only security (kept no-op under DEBUG=True) ---
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True

APPEND_SLASH = True
