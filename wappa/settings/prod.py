#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import *
import boto
import boto.s3

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# You must set ALLOWED_HOSTS if Debug is false
ALLOWED_HOSTS = ['178.62.127.105'] # ['*'] or ['127.0.0.1', 'localhost'] or [www.wappa.com]

# a bucket per author maybe
bucket_name = 'web-application-photo-bucket'

# try to get a connection to AS3
try:
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                           AWS_SECRET_ACCESS_KEY)
    # retrieve the bucket owned by me
    AS3_BUCKET = conn.get_bucket(bucket_name)
except:
    raise ImproperlyConfigured("No valid AS3 connection/bucket found")

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

# Watermarks settings
WATERMARK_BW = get_watermark("watermark-bw.jpg")

# check deploy
# https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
