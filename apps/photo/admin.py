#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from apps.photo.models import Photo, Pack, Country
from apps.photo.tasks import UploadToAS3
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _


class PhotoInline(admin.TabularInline):
    model = Photo.packs.through

class CountryAdmin(TranslatableAdmin):
    pass
    # use_fieldsets = (
    #     (_("Common"), {
    #         'fields': ('code',),
    #         }),
    #     (_("Language dependent"), {
    #         'fields': ('name',),
    #         }),
    #     )

    # def get_fieldsets(self, request, obj=None):
    #     return self.use_fieldsets

class PhotoModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        UploadToAS3.delay(obj.image.name)

class PackModelAdmin(TranslatableAdmin):
    inlines = [
        PhotoInline,
    ]
    # what's displayed in the change/read list
    #list_display = ('get_countries',)
    # def get_countries(self, obj):
    #     return "\n".join([c.lazy_translation_getter('name') for c in obj.countries.all()])

    # use_fieldsets = (
    #     (_("Common"), {
    #         'fields': ('domain', 'image',
    #                    'date published', 'pack_type', 'status', 'tags',
    #                    'begin_date', 'end_date')
    #         }),
    #     (_("Language dependent"), {
    #         'fields': ('title', 'description'),
    #         }),
    #     )

    # def get_fieldsets(self, request, obj=None):
    #     return self.use_fieldsets

admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
admin.site.register(Country, CountryAdmin)
