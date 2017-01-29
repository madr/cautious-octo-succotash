"""
Django settings for Tajm.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import dj_database_url
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('TAJM_SECRET_KEY', '-0jr90^zs@lr(0ysg05vj6rm^@#d^)r_ybqt=$jq6itm#n0sm7')

DEBUG = os.environ.get('TAJM_DEBUG', True)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'widget_tweaks',

    'tajm.httpapi',
    'tajm.dashboard',
    'frontend',
    'core',
]
ALLOWED_HOSTS = os.environ.get('TAJM_ALLOWED_HOSTS', '127.0.0.1 localhost reborn.tajm.me').split()


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'tajm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'tajm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '',
        'NAME': 'tajm_dev',
        'USER': 'ay',
        'PASSWORD': 'q1w2e3r4',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'sv-se'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# CORS Headers
# https://django-oauth-toolkit.readthedocs.org/en/latest/tutorial/tutorial_01.html
CORS_ORIGIN_ALLOW_ALL = True

# Logging
# https://docs.djangoproject.com/en/1.9/topics/logging/
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'legacy': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'httpapi': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'dashboard': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# REST Framework
# https://django-oauth-toolkit.readthedocs.org/en/latest/rest-framework/getting_started.html
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework_filters.backends.DjangoFilterBackend',),
    'PAGE_SIZE': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
}

# OAuth2 provider
# https://django-oauth-toolkit.readthedocs.org/en/latest/rest-framework/getting_started.html
OAUTH2_PROVIDER = {
    'SCOPES': {
        'reporter': 'Time reporter user centralized scope',
        'stats': 'Stats clients read-only scope',
        'management': 'Staff and superuser scope',
    },
}

# Allauth
# http://django-allauth.readthedocs.org
SITE_ID = 1
LOGIN_URL = '/id/login/'

# JSONAPI
# http://django-rest-framework-json-api.readthedocs.org/en/latest/
JSON_API_FORMAT_KEYS = 'underscore'
JSON_API_FORMAT_RELATION_KEYS = 'underscore'

# Htmlmin
# https://pypi.python.org/pypi/django-htmlmin/
# keeping HTML comments since they are useful for javascript templates.
# more on that topic: https://www.nczonline.net/blog/2011/10/11/simple-maintainable-templating-with-javascript/
KEEP_COMMENTS_ON_MINIFYING = True