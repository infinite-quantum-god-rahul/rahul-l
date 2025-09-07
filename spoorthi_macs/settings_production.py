"""
SML777 Production Settings for Render
====================================
This includes all original features with proper error handling
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-production-key')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['*', '.onrender.com', 'localhost', '127.0.0.1']

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
                'django.contrib.auth.context_processors.auth',  # Must come before custom processors
                'companies.context_processors.user_header_info',
                'companies.context_processors.sml_features',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'spoorthi_macs.wsgi.application'

# Database
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "companies/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise configuration for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Session configuration
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 14 * 24 * 3600  # Two weeks

# Cache configuration
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

# SML777 Feature Flags
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
    "RAZORPAY": {
        "KEY_ID": os.getenv("RAZORPAY_KEY_ID", ""),
        "KEY_SECRET": os.getenv("RAZORPAY_KEY_SECRET", ""),
    },
}

# SMS Configuration
SML_SMS = {
    "PROVIDER": os.getenv("SMS_PROVIDER", "TWILIO"),
    "TWILIO": {
        "ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID", ""),
        "AUTH_TOKEN": os.getenv("TWILIO_AUTH_TOKEN", ""),
        "FROM_NUMBER": os.getenv("TWILIO_FROM_NUMBER", ""),
    },
}

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

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
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}