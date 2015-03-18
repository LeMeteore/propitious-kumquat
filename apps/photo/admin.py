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
from django.http import HttpResponse, JsonResponse

from django.contrib import messages
from django import forms
from hvad.forms import TranslatableModelForm

import json
from django.shortcuts import get_object_or_404


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
            'fields': ('countries','status','date published','author',)
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
                                url(r'informations/(?P<photo_id>\d+)/$',
                                    self.admin_site.admin_view(self.informations),
                                    name='photo-informations'),)
        return custom_photo_urls + urls

    def informations(self, request, photo_id):
        if request.is_ajax():
            photo = get_object_or_404(Photo, id=photo_id)
            json_photo = {'title': photo.title,
                          'description': photo.description,
                          'image': photo.image.url}
        else:
            message = "You're the lying type, I can just tell."
        return JsonResponse(data=json_photo)

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
    use_fieldsets = (
        (_("Dates"), {
            'classes': ('collapse',),
            'fields': ('date published', 'begin_date', 'end_date',)
            }),
        (_("Images"), {
            'classes': ('extrapretty',),
            'fields': ('photos', 'image',)
            }),
        (_("Taxonomy"), {
            'classes': ('collapse',),
            'description':(_('a description fucked up')),
            'fields': ('domain', 'countries','status','pack_type','pack_tags',)
            }),
        (_("Language dependent"), {
            'classes': ('wide',),
            'fields': ('title', 'description',),
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
                                url(r'(?P<pack_id>\d+)/pack-images/$',
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
            #message = [ model_to_dict(x) for x in pack_images ]
            message = serializers.serialize(pack_images)
        else:
            message = "You're the lying type, I can just tell."
        json = json.dumps(message)
        return HttpResponse(json, mimetype='application/json')


admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
