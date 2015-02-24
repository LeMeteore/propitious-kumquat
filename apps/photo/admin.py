#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from apps.photo.models import Photo, Pack, Country
from apps.photo.tasks import UploadToAS3
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _

from django.conf.urls import patterns, url
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from django.contrib import messages
from django import forms
from hvad.forms import TranslatableModelForm

class PhotoModelAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.save()
        UploadToAS3.delay(obj.image.name)


class PackAdminForm(TranslatableModelForm):
    class Meta:
        model = Pack
        widgets = {
            'image': forms.TextInput(),
            }

class PackModelAdmin(TranslatableAdmin):
    form = PackAdminForm
    def get_urls(self):
        urls = super(PackModelAdmin, self).get_urls()
        custom_urls = patterns('',
                               url(r'(?P<pack_id>\d+)/remove_photo/(?P<photo_id>\d+)/$',
                                self.admin_site.admin_view(self.remove_photo_from_pack),
                                name='rpfp'),
                                )
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        pack = Pack.objects.get(pk=object_id)
        extra_context['current_pack'] = pack
        return super(PackModelAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def remove_photo_from_pack(self, request, photo_id, pack_id):
        messages.add_message(request, messages.SUCCESS, _('photo removed from pack with success.'))
        photo = Photo.objects.get(pk=photo_id)
        Pack.objects.get(pk=pack_id).photos.remove(photo)
        return HttpResponseRedirect(urlresolvers.reverse("admin:photo_pack_change",args=(pack_id,)))

admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
