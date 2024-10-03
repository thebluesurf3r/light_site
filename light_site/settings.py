import os
import logging.config
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'project_structure': {  # Custom logger for your application
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
logging.config.dictConfig(LOGGING)

# Add static files settings for dash apps
X_FRAME_OPTIONS = 'SAMEORIGIN'
ASGI_APPLICATION = 'light_site.routing.application'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'oauth2_provider',
    'django_filters',
    'debug_toolbar',
    'corsheaders',
    'django_celery_results',
    'channels',
#    'django_plotly_dash',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'dpd_static_support',
    'dir_scan_vis',
    'dir_scan',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'light_site.middleware.RequestLoggingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
]

PLOTLY_COMPONENTS = [
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_static_support',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

ROOT_URLCONF = 'light_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'light_site.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Celery Configuration Options
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TRACK_STARTED = True
CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'your_app.tasks.task_function',
        'schedule': 3600,  # Seconds
    },
}

# Authentication settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'accounts/login'
LOGIN_REDIRECT_URL = 'accounts/login'
LOGOUT_REDIRECT_URL = 'accounts'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5000",  # Flask App URL
]
SITE_ID = 1
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
#STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Add this line if needed


# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-secret-key')
DEBUG = env('DJANGO_DEBUG', default='True') == 'True'
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[])

CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = False  # Requires HTTPS
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = False  # Requires HTTPS

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600  # Seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'project_structure': {  # Custom logger for your application
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
