"""
Django settings for fanikisha project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv()
# import dj_database_url
import dj_database_url



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SIMPLE_JWT = {
    'AUTH_COOKIE': 'access_token',  # Cookie name for storing the access token
    'AUTH_COOKIE_SECURE': False,    # Set to True in production
    'AUTH_COOKIE_HTTP_ONLY': True,  # HTTP-only cookie to prevent JavaScript access
    'AUTH_COOKIE_PATH': '/',        # Cookie available site-wide
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Adjust SameSite settings as needed
}
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3j^*fji-gdr+gruj89k8xo_(8f8lc)34&sim-6em!!blijzn@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'farmers',
    'milkrecords',
    'api',
    'sacco',
    'cooperative',
    'corsheaders',
    'score',
    'rest_framework',
    'users',
    'authentication',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'sms',
    'django_crontab',
    "drf_yasg",
    # 'django_cron'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',



]

CORS_ALLOW_ALL_ORIGINS = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

ROOT_URLCONF = 'fanikisha.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fanikisha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
# Fallback for local development and test environments
if not os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Load Auth0 application settings into memory
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN","")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID","")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET","")
REDIRECT_URI=os.environ.get("REDIRECT_URI","")

AUTH_USER_MODEL = 'users.UserProfile'
AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

SMS_LEOPARD_API_URL = os.getenv('SMS_LEOPARD_API_URL', '')
SMS_LEOPARD_ACCESS_TOKEN = os.getenv('SMS_LEOPARD_ACCESS_TOKEN', '')



CRONJOBS = [
    ('0 8 1 *', 'sms.views.send_monthly_milk_record_sms'),
]
