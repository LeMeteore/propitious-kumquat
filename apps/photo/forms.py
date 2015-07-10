#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from hvad.forms import TranslatableModelForm
from django.contrib.auth.models import User
from apps.photo.models import Pack, Photo
from django.utils.translation import ugettext_lazy as _


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ("author", "license", "width", "height",
                  "camera_model", "sensibilite_iso", "focal",
                  "ouverture", "temps_de_pause", "countries",
                  "image", "exif_date", "pub_date", "status", "photo_tags",
                  "title", "description")

class PackForm(TranslatableModelForm):
    class Meta:
        model = Pack
        fields = ("pack_type", "title", "description", "status",
                  "pub_date", "begin_date", "end_date", "photos",
                  "pack_tags", "countries", "domain", "image")
        widgets = {
             'image': forms.TextInput(),
             }
