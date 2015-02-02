#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from datetime import datetime
from hvad.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.taxonomy.models import Country, Domain, Status, Gender

class Pack(TranslatableModel):
    pack_type = models.ForeignKey(Gender, verbose_name=_('type'))
    status = models.ForeignKey(Status, verbose_name=_('status'))

    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        description = models.CharField(max_length=200)
        )
    countries = models.ManyToManyField(Country)
    domain = models.ForeignKey(Domain, verbose_name=_('domain'))
    image = models.ImageField(max_length=200, upload_to='wappa')
    pub_date = models.DateField(default=datetime.now, name='date published')
    begin_date = models.DateField(default=datetime.now, verbose_name=_("begin_date"))
    end_date = models.DateField(default=datetime.now, verbose_name=_("end_date"))

    tags = TaggableManager()

    def __str__(self):
        return "%s" % self.lazy_translation_getter('title', str(self.pk))


class Photo(models.Model):
    title = models.CharField(max_length=200, default='un titre de photo', verbose_name=_('title'))
    description = models.CharField(max_length=200, default='une description de photo',)

    author = models.ForeignKey(User, verbose_name=_('author'))
    license = models.CharField(max_length=200, default='bsd', verbose_name=_('license'))

    countries = models.ManyToManyField(Country, verbose_name=_('countries'))
    image = models.ImageField(max_length=200, upload_to='wappa')
    pub_date = models.DateField(name='date published', default=datetime.now)
    packs = models.ManyToManyField(Pack, related_name='images')
    status = models.ForeignKey(Status, verbose_name=_('status'))

    tags = TaggableManager()

    def __str__(self):
        return "%s" % self.title
