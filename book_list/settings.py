import ast
import os.path
import warnings

from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key


def get_list(text):
    return [item.strip() for item in text.split(",")]


DEBUG = True

SITE_ID = 1

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

ROOT_URLCONF = "book_list.urls"

WSGI_APPLICATION = "book_list.wsgi.application"

_DEFAULT_CLIENT_HOSTS = "localhost,127.0.0.1"

ALLOWED_CLIENT_HOSTS = "localhost,127.0.0.1"
if not ALLOWED_CLIENT_HOSTS:
    if DEBUG:
        ALLOWED_CLIENT_HOSTS = _DEFAULT_CLIENT_HOSTS
    else:
        raise ImproperlyConfigured(
            "ALLOWED_CLIENT_HOSTS environment variable must be set when DEBUG=False."
        )

ALLOWED_CLIENT_HOSTS = get_list(ALLOWED_CLIENT_HOSTS)

INTERNAL_IPS = get_list("127.0.0.1")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


TIME_ZONE = "UTC"
LANGUAGE_CODE = "en"

context_processors = [
    "django.template.context_processors.debug",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
]

loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": context_processors,
            "loaders": loaders,
            "string_if_invalid": '<< MISSING VARIABLE "%s" >>' if DEBUG else "",
        },
    }
]

SECRET_KEY = "(th!s i5 z Sekr3t k3y)"

if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ENABLE_SSL = True
MEDIA_URL = "/media/"
STATIC_URL = "/static/"

INSTALLED_APPS = [
    # Django modules
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    # Local apps
    "book_list.book",
    "book_list.core",
    # External apps
    "graphene_django",
    "django_filters",
]

PLAYGROUND_ENABLED = True

ENABLE_DEBUG_TOOLBAR = False

ALLOWED_HOSTS = get_list("localhost,127.0.0.1")
ALLOWED_GRAPHQL_ORIGINS = get_list("*")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
OPENTRACING_MAX_QUERY_LENGTH_LOG = 10
SEARCH_BACKEND = "book_list.search.backends.postgresql"
GRAPHENE = {
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    "MIDDLEWARE": [
        "book_list.graphql.middleware.OpentracingGrapheneMiddleware",
        "book_list.graphql.middleware.JWTMiddleware",
    ],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}