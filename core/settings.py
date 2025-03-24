import sys
from decouple import config
from pathlib import Path

# ------------------------------------------------------------
# BASE SETTINGS
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key
SECRET_KEY = config('DJANGO_SECRET_KEY', '')

# Mode Depuration
DEBUG = config('DEBUG', default=True, cast=bool)

# Hosts Permitted
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# ------------------------------------------------------------
# APPLICATION DEFINITION
# ------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',

    # My Apps
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['core/base_templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------
# Altere para False no .env para usar SQLite
DOCKER_MODE = config('DOCKER_MODE', default=False, cast=bool)

if DOCKER_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

# ------------------------------------------------------------
# STATIC AND MEDIA FILES
# ------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------
# MISCELLANEOUS SETTINGS
# ------------------------------------------------------------
THOUSAND_SEPARATOR = '.'
USE_THOUSAND_SEPARATOR = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# CONFIGURAÇÃO DO BANCO DE DADOS PARA TESTES
# ------------------------------------------------------------
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db_test.sqlite3',
        }
    }
