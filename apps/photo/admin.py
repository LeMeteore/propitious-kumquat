#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from apps.photo.models import Photo, Pack, Country
from apps.photo.tasks import uploadimgtoas3, changeimgsize, generatewatermarkedimg
from celery import chain
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _

from django.conf.urls import patterns, url
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from django.contrib import messages
from django import forms
from hvad.forms import TranslatableModelForm

import json
from django.shortcuts import get_object_or_404

from .filters import StatusFilter

class PhotoModelAdmin(admin.ModelAdmin):
    use_fieldsets = (
        (_("Image"), {
            'classes': ('extrapretty',),
            'fields': ('license', 'width','height','camera_model', 'sensibilite_iso',
                       'focal', 'ouverture', 'temps_de_pause', 'image')
            }),
        (_("Taxonomy"), {
            'classes': ('collapse',),
            'description':(_('a description fucked up')),
            'fields': ('countries','status','date published','author', 'photo_tags',)
            }),
        (_("Labels"), {
            'classes': ('wide',),
            'fields': ('title', 'description',),
            }),
        )

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets

    def get_urls(self):
        urls = super(PhotoModelAdmin, self).get_urls()
        custom_photo_urls = patterns('',
                                     # example: /en/admin/photo/photo/informations/23,24,25,98/
                                    url(r'informations/(?P<photo_id>\d+(?:,(\d+))*)/$',
                                    self.admin_site.admin_view(self.informations),
                                    name='photo-informations'),)
        return custom_photo_urls + urls

    def informations(self, request, photo_id):
        # retrieve comma separated list of ids
        photo_ids_list = [int(x) for x in photo_id.split(',')]
        #json_data = []
        json_data = {}
        if request.is_ajax:
            for x in photo_ids_list:
                try:
                    p = Photo.objects.get(id=x)
                    json_data[x] = {'title': p.title,
                                    'description': p.description,
                                    'image': p.image.url}
                except:
                    json_data[x] = {"error":"not found"}
        else:
            json_data = {'error': "You're the lying type, I can just tell."}

        return JsonResponse(data=json_data)

    def save_model(self, request, obj, form, change):
        # save object first to rename change the photo name
        obj.save()
        (
        uploadimgtoas3.s(obj.image.name) |
        changeimgsize.s() |
        generatewatermarkedimg.s()
        ).apply_async()


class PackAdminForm(TranslatableModelForm):
    class Meta:
        model = Pack
        widgets = {
            'image': forms.TextInput(),
            }

class PackModelAdmin(TranslatableAdmin):
    list_filter = (StatusFilter,)
    raw_id_fields = ("photos",)
    use_fieldsets = (
        (_("Informations"), {
            'classes': ('all-span2-3',),
            'fields': ('title', 'image', 'description', 'begin_date', 'end_date',),
            }),
        (_("Sort and Display"), {
            'classes': ('all-span1-3', 'fieldset-border',),
            # 'description':(_('a description fucked up')),
            'fields': ('status', 'pack_type', 'domain', 'countries','pack_tags', 'date published')
            }),
        (_("Add Photos"), {
            'classes': ('all-span1-1',),
            'fields': ('photos',)
            }),
        )

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets


    form = PackAdminForm
    def get_urls(self):
        urls = super(PackModelAdmin, self).get_urls()
        custom_urls = patterns('',
                                url(r'(?P<pack_id>\d+)/remove-photo/(?P<photo_id>\d+)/$',
                                    self.admin_site.admin_view(self.remove_photo_from_pack),
                                    name='rpfp'),)
        custom_urls += patterns('',
                                url(r'(?P<pack_id>\d+)/images/$',
                                    self.admin_site.admin_view(self.pack_images),
                                    name='pack-images'),)
        return custom_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        pack = Pack.objects.get(pk=object_id)
        pack_images = [ x for x in pack.photos.all() ]
        extra_context['current_pack'] = pack
        extra_context['pack_images'] = pack_images
        return super(PackModelAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    def remove_photo_from_pack(self, request, photo_id, pack_id):
        messages.add_message(request, messages.SUCCESS, _('photo removed from pack with success.'))
        photo = Photo.objects.get(pk=photo_id)
        Pack.objects.get(pk=pack_id).photos.remove(photo)
        return HttpResponseRedirect(urlresolvers.reverse("admin:photo_pack_change",args=(pack_id,)))

    def pack_images(self, request, pack_id):
        if request.is_ajax():
            pack = get_object_or_404(Pack, id=pack_id)
            pack_images = pack.photos.all()
            json_data = []
            for x in pack_images:
                p = {'title': x.title, 'description': x.description, 'image': x.image.url}
                json_data.append(p)
        else:
            json_data = {"error": "You're the lying type, I can just tell."}
        # in order to allow a list (non-dict) to be serialized, set safe to false
        return JsonResponse(data=json_data, safe=False)


admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
