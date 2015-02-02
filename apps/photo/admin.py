#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from apps.photo.models import Photo, Pack, Country
from apps.photo.tasks import UploadToAS3
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _


class PhotoModelAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.save()
        UploadToAS3.delay(obj.image.name)

class PackModelAdmin(TranslatableAdmin):
    pass

admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
