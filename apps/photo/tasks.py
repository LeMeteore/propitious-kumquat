#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from celery.task import Task
from celery.registry import tasks
from celery.utils.log import get_task_logger

# Get an instance of a logger
logger = get_task_logger(__name__)

import sys
from boto.s3.key import Key
from django.conf import settings
from PIL import Image
from celery import shared_task

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


try:
    settings.AS3_BUCKET
except AttributeError:
    # we do not have a valid connection to AS3, do nothing
    @shared_task
    def uploadimgtoas3(uploadfile, **kwargs):
        pass
else:
    # we have a valid connection to AS3
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    @shared_task
    def uploadimgtoas3(uploadfile, **kwargs):
        f = os.path.join(settings.MEDIA_ROOT, uploadfile)
        k = Key(settings.AS3_BUCKET)
        # the key, should be the file name
        k.key = str(uploadfile)
        # the key value
        k.set_contents_from_filename(str(f))
        logger.info("Image {0} uploaded to AS3".format(f))
        return uploadfile

@shared_task
def changeimgsize(uploadfile, **kwargs):
    print("from uploaded img, generate another one with different size")
    # complete path to the picture
    f = os.path.join(settings.MEDIA_ROOT, uploadfile)
    # file name & extension
    fname, fext = os.path.splitext(f)
    ii = Image.open(f)
    # TODO: replace (128, 128) by a better size
    io = ii.resize((128,128))
    of = "%s%s" % (fname, fext)
    io.save(of, "jpeg")
    logger.info("New image size generated from file {0}".format(f))
    return of

@shared_task
def generatewatermarkedimg(resizedfile, **kwargs):
    print("from resized img, generate another one with a watermark")
    # complete path to the picture
    f = os.path.join(settings.MEDIA_ROOT, resizedfile)
    # file name & extension
    fname, fext = os.path.splitext(f)
    result_name_bw = "%s%s%s" % (fname, "_watermark_bw", fext)
    # complete path to watermark picture
    watermark_bw = os.path.join(settings.MEDIA_ROOT, settings.WATERMARK_BW)

    img = Image.open(f)
    wmark_bw = Image.open(watermark_bw)

    # where to paste,
    x1 = (img.size[0] - wmark_bw.size[0])/2
    y1 = (img.size[1] - wmark_bw.size[1])/2
    mask_bw = wmark_bw.convert("L").point(lambda x: min(x, 100))

    img.paste(wmark_bw, ( int(x1), int(y1)), mask_bw)
    img.save(result_name_bw, "jpeg",
             quality=50,
             optimize=True,
             progressive=True)
    logger.info("Watermarked image generated from {0}".format(f))
