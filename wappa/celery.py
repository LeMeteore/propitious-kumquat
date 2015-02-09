#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wappa.settings.dev')
app = Celery('wappa')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update()

# import the logging library
# import logging
# Get an instance of a logger
# logger = logging.getLogger(__name__)

# import sys
# import boto
# import boto.s3
# boto.set_stream_logger('boto')
# from boto.s3.key import Key

# # AWS ACCESS DETAILS
# AWS_ACCESS_KEY_ID = 'AKIAI56TPYQF65EYFULQ'
# AWS_SECRET_ACCESS_KEY = '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'

# # a bucket per author maybe
# bucket_name = 'boto-demo-1521108796'
# conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
#                        AWS_SECRET_ACCESS_KEY)
# bucket = conn.create_bucket(bucket_name,
#                             location=boto.s3.connection.Location.DEFAULT)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# def percent_cb(complete, total):
#     sys.stdout.write('.')
#     sys.stdout.flush()
#     #pass

# @app.task(bind=True)
# def uploadtoas3(self, uploadfile, **kwargs):
#     f = uploadfile
#     p = os.path.abspath(uploadfile)
#     k = Key(bucket)
#     # the key, should be the file name
#     k.key = str(f)
#     logger.debug("path %s: " % p)
#     logger.debug("file %s: " % f)
#     logger.debug('Uploading %s to Amazon S3 bucket %s' %
#                  (uploadfile, bucket_name))
#     # the key value
#     k.set_contents_from_filename(p,
#                                  cb=percent_cb,
#                                  num_cb=10)


# @app.task(bind=True)
# def resizeimage(self, uploadfile, **kwargs):
#     pass


# @app.task(bind=True)
# def removeoriginaleimage(self, **kwargs):
#     pass
