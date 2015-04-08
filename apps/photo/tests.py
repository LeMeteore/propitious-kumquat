#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.test import TestCase
from apps.photo.models import Pack, Photo
from apps.taxonomy.models import Country, Domain, Status, Gender
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your tests here.
class MyTest(TestCase):
    def setUp(self):
        u = User.objects.create()
        s = Status.objects.create()
        t = Gender.objects.create()
        d = Domain.objects.create()
        c = Country.objects.language('en').create(name='Senegal', code='SN')
        self.user = u
        self.status = s
        self.country = c
        self.domain = d
        self.type = t

    def create_photo(self, pk):
        my_home = os.environ['HOME']
        filename = "Images/mandelbrot_shrodinger_cat.jpg"
        file_to_upload = os.path.join(my_home, filename)
        f = File(open(file_to_upload, 'rb'))
        # the photo to upload
        p = Photo(title = "une photo de test",
                  description = "description d'une photo de test",
                  author = self.user,
                  license = "une license de test",
                  width = 100,
                  height = 100,
                  camera_model = "un modele de camera de test",
                  sensibilite_iso = "une sensibilité iso de test",
                  focal = "focal de test",
                  ouverture = "ouverture de test",
                  temps_de_pause = "temps de pause de test",
                  status = self.status,
                  id = pk
                  )
        p.image.save("mandelbrot_shrodinger_cat.jpg", f)
        # p should be saved first before adding m2m relations
        p.countries.add(self.country)
        return p



class PhotoTest(MyTest):
    def test_photo_creation(self):
        p = self.create_photo(pk=5)
        self.assertTrue(isinstance(p, Photo))
        self.assertEqual(p.__str__(), p.title)


class PackTest(MyTest):
    def create_pack(self):
        photo = self.create_photo(pk=8)
        p = Pack.objects.language('en').create(title = "une pack de test",
                                                description = "description d'une pack de test",
                                                pack_type = self.type,
                                                status = self.status,
                                                domain = self.domain,
                                                image = photo,
                                                id = 5
                  )

        # p should be saved first before adding m2m relations
        p.countries.add(self.country)
        p.photos.add(photo)
        return p

    def test_pack_creation(self):
        p = self.create_pack()
        self.assertTrue(isinstance(p, Pack))
        self.assertEqual(p.__str__(), p.title)
