#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# You must set ALLOWED_HOSTS if Debug is false
ALLOWED_HOSTS = ['178.62.127.105'] # ['*'] or ['127.0.0.1', 'localhost'] or [www.wappa.com]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wappa',
        'USER': 'wappa',
        'PASSWORD': '75708787712200040608',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        }
}

# You can turn on cached loading for templates
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        )),
)
