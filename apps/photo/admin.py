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
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        pack_photos = Pack.objects.get(pk=object_id).photos.all()
        extra_context['pack_photos'] = pack_photos
        return super(PackModelAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
