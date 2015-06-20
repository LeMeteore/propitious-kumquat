#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import *
import boto
import boto.s3

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# a bucket per author maybe
bucket_name = 'web-application-photo-bucket'

# try to get a connection to AS3
try:
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                           AWS_SECRET_ACCESS_KEY)
    # retrieve the bucket owned by me
    bucket = conn.get_bucket(bucket_name)
except:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST_NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

import django
if django.conf.settings.DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIAL_URL = '/media/'
    WATERMARK_BW = os.path.join(MEDIA_ROOT, "wappa", "watermark-bw.jpg")

# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
    'template_debug',
)

class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

TEST_IN_PROGRESS = False


# if debug, do not put media root under /var/www
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIAL_URL = '/media/'
WATERMARK_BW = os.path.join(MEDIA_ROOT, "wappa", "watermark-bw.jpg")

# if debug, is this config for email server
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@wappa.com'



if 'test' in sys.argv[1:] or 'jenkins' or 'test_coverage' in sys.argv[1:]:
    TESTS_IN_PROGRESS = True
    MIGRATION_MODULES = DisableMigrations()
