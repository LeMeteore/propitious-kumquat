"""
Django settings for wappa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# the directory containing the manage.py file
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

# add ROOT_DIR to the python path
import sys
sys.path.append(ROOT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'c8o8m)ztlose*7t4)1h_du$mi52=bu%ug3fztu8ah2&#1f!$6z'

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ.get(var_name)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

def get_secret_from_file(secret_file):
    try:
        return open(os.path.join(BASE_DIR, secret_file)).read().strip()
    except KeyError:
        error_msg = "Secret file %s missing" % secret_file
        raise ImproperlyConfigured(error_msg)


#SECRET_KEY = get_env_variable('SECRET_KEY')
#SECRET_KEY = open(os.path.join(BASE_DIR, 'settings/secret.txt')).read().strip()
SECRET_KEY = get_secret_from_file('settings/secret.txt')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.photo',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wappa.urls'

WSGI_APPLICATION = 'wappa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    )

# Media files ( user uploaded contents)
# https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = "/var/www/wappa/media/"

MEDIA_URL = "/media/"
