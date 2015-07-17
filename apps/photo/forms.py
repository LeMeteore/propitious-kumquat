#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from apps.photo.models import Pack, Photo, PackTranslation
from django.utils.translation import ugettext_lazy as _


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ("author", "license", "width", "height",
                  "camera_model", "sensibilite_iso", "focal",
                  "ouverture", "temps_de_pause", "countries",
                  "image", "exif_date", "pub_date", "status", "photo_tags",
                  "title", "description")


class BasePackForm(ModelForm):

    class Meta:
        model = Pack
        fields = ("pack_type", "status",
                  "pub_date", "begin_date", "end_date", "photos",
                  "pack_tags", "countries", "domain", "image")
        widgets = {
             'image': forms.TextInput(),
             'photos': forms.TextInput(),
             }

class PackForm(BasePackForm):
    title_fr = forms.CharField(label=_("French Title"),
                               widget=forms.TextInput,
                               required=True,
                               help_text=_('French Title'),)
    description_fr = forms.CharField(label=_("French Description"),
                                     widget=forms.Textarea,
                                     required=True,
                                     help_text=_('French Description'))
    title_en = forms.CharField(label=_("English Title"),
                               widget=forms.TextInput,
                               required=True,
                               help_text=_('English Title'))
    description_en = forms.CharField(label=_("English Description"),
                                     widget=forms.Textarea,
                                     required=True,
                                     help_text=_('English Description'))

    class Meta(BasePackForm.Meta):
        fields = BasePackForm.Meta.fields + ('title_fr', 'description_fr', 'title_en', 'description_en')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['photos'].choices = [(x[0],str(x[0])) for x in Photo.objects.values_list('id')]
        # self.fields['image'].choices = [(x[0],str(x[0])) for x in Photo.objects.values_list('id')]

        if 'instance' in kwargs:
            pck = kwargs.pop('instance')
            if pck.id:
                #self.fields['photos'].queryset = pck.photos.values_list('id')
                try:
                    self.fields['title_fr'].initial = pck.translations.get_language('fr').title
                    self.fields['title_en'].initial = pck.translations.get_language('en').title
                    self.fields['description_fr'].initial = pck.translations.get_language('fr').description
                    self.fields['description_en'].initial = pck.translations.get_language('en').description
                except:
                    pass

    def clean(self):
        self.cleaned_data = super().clean()
