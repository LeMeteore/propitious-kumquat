#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from apps.photo.models import Photo, Pack
from apps.photo.tasks import UploadToAS3
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _

class PhotoModelAdmin(TranslatableAdmin):
    use_fieldsets = (
        (_("Common"), {
            'fields': ('pack', 'country', 'image',
                       'date published', 'status',)
            }),
        (_("Language dependent"), {
            'fields': ('label', 'description', 'tags',),
            }),
        )

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets

    def save_model(self, request, obj, form, change):
        obj.save()
        UploadToAS3.delay(obj.image.name)


class PackModelAdmin(TranslatableAdmin):
    use_fieldsets = (
        (_("Common"), {
            'fields': ('domain', 'country', 'image',
                       'date published', 'pack_type', 'status',)
            }),
        (_("Language dependent"), {
            'fields': ('label', 'description', 'tags'),
            }),
        )

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets

admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
