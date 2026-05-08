import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set — add it to your .env file (see .env.example)")

DEBUG = os.environ.get('DEBUG', 'True').lower() not in ('false', '0')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MainApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'MainApp.middleware.VisitTrackerMiddleware',
]

ROOT_URLCONF = 'portfolio_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_site.wsgi.application'

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '')
USE_CLOUDINARY = CLOUDINARY_URL.startswith('cloudinary://')

if USE_CLOUDINARY:
    INSTALLED_APPS += ['cloudinary_storage', 'cloudinary']

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
    'default': {
        'BACKEND': (
            'cloudinary_storage.storage.MediaCloudinaryStorage'
            if USE_CLOUDINARY else
            'django.core.files.storage.FileSystemStorage'
        ),
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'MainApp' / 'media'

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email
GMAIL_ADDRESS       = os.environ.get('GMAIL_ADDRESS', '')
GMAIL_APP_PASS      = os.environ.get('GMAIL_APP_PASS', '')
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = GMAIL_ADDRESS
EMAIL_HOST_PASSWORD = GMAIL_APP_PASS
DEFAULT_FROM_EMAIL  = GMAIL_ADDRESS or 'noreply@portfolio.com'
ADMIN_EMAIL         = 'omoladedaniel@gmail.com'

# Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Google Calendar
GCAL_CREDENTIALS_PATH = os.environ.get('GCAL_CREDENTIALS_PATH', '')
GCAL_CALENDAR_ID      = os.environ.get('GCAL_CALENDAR_ID', 'primary')
GCAL_TIMEZONE         = os.environ.get('GCAL_TIMEZONE', 'UTC')

LOGIN_URL = '/admin/login/'
