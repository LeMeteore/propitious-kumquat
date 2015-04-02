#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

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


MEDIA_ROOT = "/var/www/wappa/media/" or os.path.join(BASE_DIR, 'media')

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

if 'test' in sys.argv[1:] or 'jenkins' or 'test_coverage' in sys.argv[1:]:
    TESTS_IN_PROGRESS = True
    MIGRATION_MODULES = DisableMigrations()
