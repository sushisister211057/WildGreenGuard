"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import json
from dotenv import load_dotenv

# load .env variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-cs9xr^ev95*y4fi3tryl-3)h67gn(y#wmavseo+8jf(2a$97=l"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "plants",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # Csrf Middleware is added
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.LanguageMiddleware"
]

ROOT_URLCONF = "myproject.urls"

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

WSGI_APPLICATION = "myproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'plants',
    #     'USER': 'root',
    #     'PASSWORD': 'test123',
    #     'HOST': '35.202.57.198',  # Or an IP Address that your DB is hosted on
    #     'PORT': '3308',  # Default MySQL port
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'plants',
        'USER': 'root',
        'PASSWORD': 'mysql123',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',  # Default MySQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOGIN_URL = "/plants/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR , "static"),
]

# Media files

# Base url to serve media files
MEDIA_URL = '/media/'
# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# set auth usermodel

AUTH_USER_MODEL = "users.CustomUserModel"
AUTHENTICATION_BACKENDS = ["users.backends.CustomUserModelBackend"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Line related url
# for line login
LINE_LOGIN_SECRET = "67bf2a23e51e07eb4d4dd34830f68d67"
LINE_LOGIN_ENDPOINT = "https://ce5e-2001-b400-e35d-9b93-70ec-4cac-94f-409f.ngrok-free.app"
LINE_LOGIN_ENDPOINT += "/users/line_login"
LINE_LOGIN_ID = 2002587486
# for line api
LINE_API_URL = ""


# translate json 
TRANS_REPO = {}
TRANS_DICT = {}

if not TRANS_REPO:
    trans_path = f"{BASE_DIR}/plants/static/plants/json/translate.json"
    with Path(trans_path).open("r", encoding="utf-8") as f:
        TRANS_REPO = json.load(f)
        TRANS_DICT = {k:v[0] for k, v in TRANS_REPO.items()}