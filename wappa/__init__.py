#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
# app is always imported when django starts
from .celery import app as celery_app
