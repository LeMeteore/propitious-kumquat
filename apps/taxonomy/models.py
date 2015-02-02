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

class Domain(TranslatableModel):
    """A pack is defined by its domain
    a domain could be: ...
    """
    translations = TranslatedFields(
        name = models.CharField(max_length=200)
        )

    def __str__(self):
        return "%s" % self.lazy_translation_getter('name', str(self.pk))

    class Meta:
        verbose_name = _("domain")
        verbose_name_plural = _("domains")

class Status(TranslatableModel):
    """A pack is defined by its status
    a status could be: online, offline, ...
    """
    translations = TranslatedFields(
        name = models.CharField(max_length=200)
        )

    def __str__(self):
        return "%s" % self.lazy_translation_getter('name', str(self.pk))

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statuses")

class Gender(TranslatableModel):
    """A pack is defined by its type.
    a type could be: actualite, reportage, ...
    """
    translations = TranslatedFields(
        name = models.CharField(max_length=200)
        )

    def __str__(self):
        return "%s" % self.lazy_translation_getter('name', str(self.pk))

    class Meta:
        verbose_name = _("type")
        verbose_name_plural = _("types")
