#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Django settings for wappa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _

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

def get_as3_credentials_from_file(secret_file):
    try:
        return [line.strip() for line in open(os.path.join(BASE_DIR, secret_file))]
    except KeyError:
        error_msg = "AS3 credentials file %s missing" % secret_file
        raise ImproperlyConfigured(error_msg)

#SECRET_KEY = get_env_variable('SECRET_KEY')
#SECRET_KEY = open(os.path.join(BASE_DIR, 'settings/secret.txt')).read().strip()
SECRET_KEY = get_secret_from_file('settings/secret.txt')
AWS_ACCESS_KEY_ID = get_as3_credentials_from_file('settings/as3_secret.txt')[0]
AWS_SECRET_ACCESS_KEY = get_as3_credentials_from_file('settings/as3_secret.txt')[1]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my apps
    'apps.photo',
    'apps.taxonomy',
    'hvad',
    'taggit',
    'celery',
    'imagekit',
)

# https://docs.djangoproject.com/en/1.7/topics/http/middleware/
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
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

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://docs.djangoproject.com/en/1.7/topics/i18n/timezones/
TIME_ZONE = 'Africa/Dakar'

# languages that we want to use for translations
# http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)

#
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locales"),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/1.7/ref/settings/#static-root
# absolute path to directory where collectstatic will collect static files 4 deployment.
STATIC_ROOT = "/var/www/wappa/static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    )

# templates context processors
# https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS

# Media files ( user uploaded contents)
# https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = "/var/www/wappa/media/"

MEDIA_URL = "/media/"

# Celery settings
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Logging configuration only works if the DEBUG = False ?!?!?!
#
LOGGING_CONFIG = None
LOGFILE_SIZE = 50000
# Log file count
LOGFILE_COUNT = 10
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S",
            },
        'simple': {
            'format': '%(levelname)s %(asctime) %(module) %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S",
            },
        },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
            },
        'syslog': {
            'level':'DEBUG',
            'class':'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'facility': 'logging.handlers.SysLogHandler.LOG_LOCAL2',
            },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
            },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "logs/django.log"),
            'formatter': 'simple'
            },
        'django_rotate': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs/django_rotate.log"),
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            },
        'django_requests': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "logs/django_requests.log"),
            },
        'apps': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "logs/apps.log"),
            'formatter': 'simple'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['django_requests'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'django': {
                'handlers': ['django'],
                'level': 'DEBUG',
                'propagate': True,
                },
            'apps.photo': {
                'handlers': ['apps'],
                'level': 'DEBUG',
                'propagate':True,
            },
        },
    }


import logging.config
logging.config.dictConfig(LOGGING)
