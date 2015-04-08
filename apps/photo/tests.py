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
class PhotoTest(TestCase):
    def setUp(self):
        u = User()
        u.save()
        s = Status()
        s.save()
        c = Country.objects.language('en').create(name='Senegal', code='SN')
        c.save()
        self.user = u
        self.status = s
        self.country = c

    def create_photo(self):
        # the photo to upload
        my_home = os.environ['HOME']
        filename = "Images/mandelbrot_shrodinger_cat.jpg"
        file_to_upload = os.path.join(my_home, filename)
        f = File(open(file_to_upload, 'rb'))
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
                  id = 5
                  )
        p.image.save("mandelbrot_shrodinger_cat.jpg", f)
        # p should be saved first before adding m2m relations
        p.countries.add(self.country)
        return p

    def test_photo_creation(self):
        p = self.create_photo()
        self.assertTrue(isinstance(p, Photo))
        self.assertEqual(p.__str__(), p.title)
