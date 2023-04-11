"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import timedelta

AUTH_USER_MODEL = "user_app.User"
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ee)niv++_^vm(t&c$f8gcq=%i*qtatpe1_u)_&3*7*)9x&m#%k"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
DEFAULT_CURRENCY = "USD"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # packages
    "rest_framework",
    "rest_framework.authtoken",
    "knox",
    "djoser",
    "drf_spectacular",
    "django_extensions",
    # apps
    "user_app",
    "user_payment",
    "product",
    "order",
    "sending_mail",
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
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    # TODO for check user login ceredetual
    # "DEFAULT_AUTHENTICATION_CLASSES": (
    #     "rest_framework.authentication.TokenAuthentication",
    # ),
    "DEFAULT_AUTHENTICATION_CLASSES": ("user_app.auth.CustomTokenAuthentication",),
    # TODO for django filters
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATETIME_INPUT_FORMAT": "%Y-%m-%d %H:%M:%S",
}


DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {
        "user": "user_app.serializers.UserSerializers",
        "current_user": "user_app.serializers.UserSerializers",
        "user_create": "user_app.serializers.CustomUserCreateSerializer",
        # "user_delete": "accounts.serializers.UserDeleteSerializer",
        # "password_reset": "accounts.serializers.SendEmailResetSerializer",
    },
}


REST_KNOX = {
    "USER_SERIALIZER": "user_app.serializers.UserSerializers",
    "TOKEN_TTL": timedelta(hours=48),
}


PRODUCT_PRICE = "price_1Mf1U0JXetuhxuuut3u5Hrml"
STRIPE_SECRET_KEY_TEST = "sk_test_51MY6sxJXetuhxuuuy8bCW69gDQGDcAKzR50zwnNiRRLjr1awpf4EFgDJypUNcDXpiBinrQ9KLVvO3eDI4c8AHhuY00g2QzFWfB"
STRIPE_WEBHOOK_SECRET_TEST = (
    "whsec_4c6008dff57b6823b2425d44bafde151d17a1f23618a936b5c6a6db60e0ed4ee"
)


# --------------- celery -------------------- #
CELERY_BROKER_URL = "redis://127.0.0.1:6379"  # redis end_point
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Cairo"

CELERY_RESULT_BACKEND = "django-db"

# ------------- email config --------------------- #
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "abdallaamer101@gmail.com"
EMAIL_HOST_PASSWORD = "wbmpmpgbyqmpghuo"
DEFAULT_FROM_EMAIL = "default from email"
