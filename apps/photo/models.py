#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from datetime import datetime
from hvad.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from apps.photo import choices
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Country(TranslatableModel):
    code = models.CharField(max_length=2, primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=200)
        )

    def __str__(self):
        return "%s" % self.lazy_translation_getter('name', str(self.pk))

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

class Pack(TranslatableModel):
    pack_type = models.CharField(max_length=200,
                                choices=choices.PACK_TYPE_CHOICES,
                                default=choices.ACTUALITE,
                                verbose_name="type")
    status = models.CharField(max_length=200,
                              choices=choices.STATUS_CHOICES,
                              default=choices.OFFLINE)

    translations = TranslatedFields(
        title = models.CharField(max_length=200),
        description = models.CharField(max_length=200)
        )
    countries = models.ManyToManyField('Country')
    domain = models.CharField(max_length=200)
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

    author = models.ForeignKey(User, default=1, verbose_name=_('author'))
    license = models.CharField(max_length=200, default='bsd', verbose_name=_('license'))

    countries = models.ManyToManyField(Country, verbose_name=_('countries'))
    image = models.ImageField(max_length=200, upload_to='wappa')
    pub_date = models.DateField(name='date published', default=datetime.now)
    packs = models.ManyToManyField(Pack, related_name='images')
    status = models.CharField(max_length=200,
                              choices=choices.STATUS_CHOICES,
                              default=choices.OFFLINE,
                              verbose_name=_('status'))
    tags = TaggableManager()

    def __str__(self):
        return "%s" % self.title
