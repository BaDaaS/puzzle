"""
Django settings for puzzle project.
"""

from pathlib import Path
from decouple import config, RepositoryEnv, Config
import logging

# Can be used to load a different .env
DECOUPLE_CONFIG_FILE = config("DECOUPLE_ENVFILE", default=".env")
config = Config(RepositoryEnv(DECOUPLE_CONFIG_FILE))

logging.basicConfig(level=logging.INFO)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "trading",
    "common",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

ROOT_URLCONF = "puzzle.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "puzzle.wsgi.application"

# ----------------- DATABASE -----------------
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASE_ENGINE = config("DB_ENGINE")
if DATABASE_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {"ENGINE": config("DB_ENGINE"), "NAME": BASE_DIR / config("DB_NAME")}
    }
elif DATABASE_ENGINE == "django.db.backends.postgresql_psycopg2":
    DATABASES = {
        "default": {
            "ENGINE": config("DB_ENGINE"),
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        }
    }
else:
    raise ValueError(f"Unsupported database engine: {DATABASE_ENGINE}")

# ----------------- DATABASE -----------------


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# ----------------- I18N -----------------
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
# ----------------- I18N -----------------


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ----------------- ACCOUNTING APP -----------------
# 0 = base account name
# 1 = currency symbol
# 2 = entity name
DEFAULT_NAME_FORMAT_ACCOUNT_EXPENSES = "{0} ({1} - {2})"
# ----------------- ACCOUNTING APP -----------------


# ----------------- TRADING APP -----------------
# Crypto Exchange Trading
CRYPTO_EXCHANGE_KRAKEN_API_KEY = config("CRYPTO_EXCHANGE_KRAKEN_API_KEY", default=None)
CRYPTO_EXCHANGE_KRAKEN_SECRET_KEY = config(
    "CRYPTO_EXCHANGE_KRAKEN_SECRET_KEY", default=None
)

# Coinbase Pro
CRYPTO_EXCHANGE_COINBASE_PRO_API_KEY = config(
    "CRYPTO_EXCHANGE_COINBASE_PRO_API_KEY", default=None
)
CRYPTO_EXCHANGE_COINBASE_PRO_SECRET_KEY = config(
    "CRYPTO_EXCHANGE_COINBASE_PRO_SECRET_KEY", default=None
)

CRYPTO_EXCHANGE_COINBASE_PRO_PASSWORD = config(
    "CRYPTO_EXCHANGE_COINBASE_PRO_PASSWORD", default=None
)

# Coinbase
CRYPTO_EXCHANGE_COINBASE_API_KEY = config(
    "CRYPTO_EXCHANGE_COINBASE_API_KEY", default=None
)
CRYPTO_EXCHANGE_COINBASE_SECRET_KEY = config(
    "CRYPTO_EXCHANGE_COINBASE_SECRET_KEY", default=None
)
# ----------------- TRADING APP -----------------

# ----------------- INFRASTRUCTURE -----------------
# Redis settings
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = config("REDIS_PORT", cast=int)
# #FIXME: not used at the moment.
REDIS_USER = config("REDIS_USER", default=None)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
# ----------------- INFRASTRUCTURE -----------------

INTERNAL_IPS = [
    "127.0.0.1",
]
