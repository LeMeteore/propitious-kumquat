#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from celery.task import Task
from celery.registry import tasks
#from celery.utils.log import get_task_logger

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

import sys
import boto
import boto.s3
boto.set_stream_logger('boto')
from boto.s3.key import Key



from django.conf import settings

class UploadToAS3(Task):

    # AWS ACCESS DETAILS
    AWS_ACCESS_KEY_ID = 'AKIAI56TPYQF65EYFULQ'
    AWS_SECRET_ACCESS_KEY = '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'

    # a bucket per author maybe
    bucket_name = 'web-application-photo-bucket'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                        AWS_SECRET_ACCESS_KEY)
    #bucket = conn.create_bucket(bucket_name,
    #                            location=boto.s3.connection.Location.DEFAULT)

    # retrieve the bucket owned by me
    bucket = conn.get_bucket(bucket_name)

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
        #pass

    def run(self, uploadfile, **kwargs):
        f = os.path.join(settings.MEDIA_ROOT, uploadfile)
        k = Key(self.bucket)
        # the key, should be the file name
        k.key = str(uploadfile)
        # the key value
        k.set_contents_from_filename(str(f))

class ReduceImageSize(Task):
    def run(self, uploadfile, **kwargs):
        f = os.path.join(settings.MEDIA_ROOT, uploadfile)
        # generer plusieurs images de differentes tailles
        # et pour chaque images, appliquer le filigrane



class RemoveOriginalImage(Task):
    def run(self, **kwargs):
        pass

tasks.register(UploadToAS3)
tasks.register(ReduceImageSize)
tasks.register(RemoveOriginalImage)
