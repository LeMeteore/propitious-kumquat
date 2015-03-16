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
from boto.s3.key import Key

from django.conf import settings
from PIL import Image

class UploadToAS3(Task):

    # AWS ACCESS DETAILS
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

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

class GenerateReducedImage(Task):
    def run(self, **kwargs):
        pass

class GenerateImageWatermarked(Task):
    def run(self, uploadfile, **kwargs):
        # complete path to the picture
        f = os.path.join(settings.MEDIA_ROOT, uploadfile)
        # file name & extension
        fname, fext = os.path.splitext(f)
        result_name = "%s%s%s" % (fname, "_watermark", fext)
        # complete path to watermark picture
        watermark = os.path.join(settings.MEDIA_ROOT, settings.WATERMARK1)

        img = Image.open(f)
        wmark = Image.open(watermark)
        # where to paste
        x1 = (img.size[0] - wmark.size[0])/2
        y1 = (img.size[1] - wmark.size[1])/2
        mask = wmark.convert("L").point(lambda x: min(x, 75))

        img.paste(wmark, ( int(x1), int(y1)), mask)
        img.save(result_name, "jpeg",
                 quality=50,
                 optimize=True,
                 progressive=True)

class RemoveOriginalImage(Task):
    def run(self, **kwargs):
        pass

tasks.register(UploadToAS3)
tasks.register(GenerateReducedImage)
tasks.register(GenerateImageWatermarked)
tasks.register(RemoveOriginalImage)
