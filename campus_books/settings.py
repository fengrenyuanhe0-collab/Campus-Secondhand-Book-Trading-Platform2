from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-campus-books-2024-change-in-production')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:1234',
    'http://127.0.0.1:1234',
    'http://localhost',
    'http://127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'books.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'campus_books.urls'

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

WSGI_APPLICATION = 'campus_books.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('POSTGRES_DB',       'campus_books'),
        'USER':     os.environ.get('POSTGRES_USER',     'campus'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'campus_pass'),
        'HOST':     os.environ.get('POSTGRES_HOST',     'db'),
        'PORT':     os.environ.get('POSTGRES_PORT',     '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True

# ── Redis Cache ───────────────────────────────────────────────────────────────
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/1')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            'socket_connect_timeout': 2,
            'socket_timeout': 2,
        },
    }
}

# ── Email (console backend for demo — prints reset link to logs) ──────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@campus-books.example'

# ── Logging ───────────────────────────────────────────────────────────────────
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'app_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'app.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'error.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'books': {
            'handlers': ['app_file', 'error_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users': {
            'handlers': ['app_file', 'error_file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/'
