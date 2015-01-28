#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from datetime import datetime
from hvad.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from apps.photo import choices


class Entity(TranslatableModel):
    tags = TaggableManager()
class Country(TranslatableModel):
    code = models.CharField(max_length=2, primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=200)
        )

    def __str__(self):
        return "%s" % self.lazy_translation_getter('name', str(self.pk))

class Pack(Entity):
    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    pack_type = models.CharField(max_length=200,
                                choices=choices.PACK_TYPE_CHOICES,
                                default=choices.ACTUALITE,
                                verbose_name="type")
    status = models.CharField(max_length=200,
                              choices=choices.STATUS_CHOICES,
                              default=choices.OFFLINE)

    translations = TranslatedFields()
    country = models.ManyToManyField(Country)
    domain = models.CharField(max_length=200)
    image = models.ImageField(max_length=200, upload_to='wappa')
    pub_date = models.DateField(default=datetime.now, name='date published')


    def __str__(self):
        return "%s" % self.lazy_translation_getter('label', str(self.pk))

class Photo(Entity):

    translations = TranslatedFields()
    country = models.ManyToManyField(Country)
    image = models.ImageField(max_length=200, upload_to='wappa')
    pub_date = models.DateField(name='date published', default=datetime.now)
    pack = models.ManyToManyField(Pack)
    status = models.CharField(max_length=200,
                              choices=choices.STATUS_CHOICES,
                              default=choices.OFFLINE,
                              verbose_name=_('status'))

    def __str__(self):
        return "%s" % self.safe_translation_getter('label', str(self.pk))


#    def default_country(self):
