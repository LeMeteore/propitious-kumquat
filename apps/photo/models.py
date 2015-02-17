#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from datetime import datetime
from hvad.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.taxonomy.models import Country, Domain, Status, Gender

from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

import os

class Photo(models.Model):

    def content_file_name(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s_%s_%s%s%s.%s" % (instance.author_id,
                                        instance.title.replace (" ", "_"),
                                        instance.width, "x", instance.height,
                                        ext)
        return os.path.join('wappa', filename)

    title = models.CharField(max_length=200, verbose_name=_('title'))
    description = models.TextField(max_length=200, verbose_name=_('description'))

    author = models.ForeignKey(User, verbose_name=_('author'))
    license = models.CharField(max_length=200, verbose_name=_('license'))
    width = models.IntegerField(max_length=200, verbose_name=_('width'))
    height = models.IntegerField(max_length=200, verbose_name=_('heigth'))
    camera_model = models.CharField(max_length=200, verbose_name=_('camera_model'))
    sensibilite_iso = models.CharField(max_length=200, verbose_name=_('sensibilite_iso'))
    focal = models.CharField(max_length=200, verbose_name=_('focal'))
    ouverture = models.CharField(max_length=200, verbose_name=_('ouverture'))
    temps_de_pause = models.CharField(max_length=200, verbose_name=_('temps_de_pause'))
    countries = models.ManyToManyField(Country, verbose_name=_('countries'))
    image = models.ImageField(max_length=200, upload_to=content_file_name)
    pub_date = models.DateField(name='date published', default=datetime.now)
    status = models.ForeignKey(Status, verbose_name=_('status'))

    photo_tags = TaggableManager(blank=True)

    def __str__(self):
        return "%s" % self.title

    def get_change_urls(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label,
                                                            content_type.model),
                                                            args=(self.id,))


class Pack(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=200, verbose_name=_('title')),
        description = models.TextField(max_length=200, verbose_name=_('description'))
        )
    pack_type = models.ForeignKey(Gender, verbose_name=_('type'))
    status = models.ForeignKey(Status, verbose_name=_('status'))
    countries = models.ManyToManyField(Country)
    domain = models.ForeignKey(Domain, verbose_name=_('domain'))
    image = models.ForeignKey(Photo, null=True, blank=True, verbose_name=_('image preview'))

    pub_date = models.DateField(default=datetime.now, name='date published')
    begin_date = models.DateField(default=datetime.now, verbose_name=_("begin_date"))
    end_date = models.DateField(default=datetime.now, verbose_name=_("end_date"))

    photos = models.ManyToManyField(Photo, null=True, blank=True, related_name='packs')

    pack_tags = TaggableManager(blank=True)

    def __str__(self):
        return "%s" % self.lazy_translation_getter('title', str(self.pk))

    def get_change_urls(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
