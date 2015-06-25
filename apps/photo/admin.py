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
from django.core.paginator import Paginator, EmptyPage
from django.core.paginator import PageNotAnInteger
from .filters import StatusFilter

class PhotoModelAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None, ):
        extra_context = extra_context or {}
        # TODO: retrieve only needed fields
        #photos = [(x.title, x.description, x.image.name) for x in Photo.objects.all()]
        # photos = [{'title': x.title,
        #            'id': x.id,
        #            'description': x.description,
        #            'image': x.image.name} for x in Photo.objects.all()]
        photos_list = [x for x in Photo.objects.all()]
        paginator = Paginator(photos_list, 10) # 10 photos per page
        page = request.GET.get('page')

        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)

        extra_context['photos_list'] = photos
        return super().changelist_view(request,
                                       extra_context=extra_context)
    use_fieldsets = (
        (_("Photo"), {
            'classes': ('all-span1-4',),
            'fields': ('image', 'camera_model', 'width','height',
                       'focal', 'ouverture', 'temps_de_pause', 'sensibilite_iso', 'license' )
            }),
        (_("Fields"), {
            'classes': ('all-span3-4',),
            'fields': ('title', 'description','author',
                       'countries', 'status', 'photo_tags', 'pub_date')
            })
        )

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets

    def get_urls(self):
        urls = super().get_urls()
        custom_photo_urls = patterns('',
                                     # example: /en/admin/photo/photo/informations/23,24,25,98/
                                    url(r'informations/(?P<photo_id>\d+(?:,(\d+))*)/$',
                                    self.admin_site.admin_view(self.informations),
                                    name='photo-informations'),)
        return custom_photo_urls + urls

    def informations(self, request, photo_id):
        # retrieve comma separated list of ids
        photo_ids_list = [int(x) for x in photo_id.split(',')]
        json_data = []
        #json_data = {}
        if request.is_ajax:
            for x in photo_ids_list:
                try:
                    p = Photo.objects.get(id=x)
                    # json_data[x] = {'title': p.title,
                    #                 'description': p.description,
                    #                 'image': p.image.url}
                    pp = {'id': p.id,
                          'status': p.status.lazy_translation_getter('name'),
                          'title': p.title,
                          'description': p.description,
                          'image': p.image.url,
                          'date published': getattr(p, 'date published').strftime("%d-%m-%Y"),}
                    json_data.append(pp)
                except:
                    pp = {"error":"not found"}
                    json_data.append(pp)
        else:
            json_data.append({'error': "You're the lying type, I can just tell."})

        return JsonResponse(data=json_data, safe=False)

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
        urls = super().get_urls()
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
        # TODO: retrieve only needed fields
        pack_images = [ x for x in pack.photos.all() ]
        extra_context['current_pack'] = pack
        extra_context['pack_images'] = pack_images
        return super().change_view(request,
                                   object_id,
                                   form_url,
                                   extra_context=extra_context)


    def remove_photo_from_pack(self, request, photo_id, pack_id):
        messages.add_message(request, messages.SUCCESS, _('photo removed from pack with success.'))
        photo = Photo.objects.get(pk=photo_id)
        Pack.objects.get(pk=pack_id).photos.remove(photo)
        return HttpResponseRedirect(urlresolvers.reverse("admin:photo_pack_change",args=(pack_id,)))

    def pack_images(self, request, pack_id):
        if request.is_ajax():
            pack = get_object_or_404(Pack, id=pack_id)
            #pack_images = pack.photos.all().values(*["id", "title", "description", "image", "date published"])
            pack_images = pack.photos.all()
            json_data = list()
            for x in pack_images:
                p = {'id': x.id,
                     'status': x.status.lazy_translation_getter('name'),
                     'title': x.title,
                     'description': x.description,
                     'image': x.image.url,
                     'date published': getattr(x, 'date published').strftime("%d-%m-%Y"),}
                json_data.append(p)
        else:
            json_data = {"error": "You're the lying type, I can just tell."}
        # in order to allow a list (non-dict) to be serialized, set safe to false
        return JsonResponse(data=json_data, safe=False)


admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Pack, PackModelAdmin)
