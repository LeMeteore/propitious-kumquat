#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.test import TestCase, Client
from apps.photo.models import Pack, Photo
from apps.taxonomy.models import Country, Domain, Status, Gender
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse



class BackOfficeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {'username':'patrick',
                            'password':'patrick'}
        # a user should exist to test login
        User.objects.create_user(**self.credentials)

    def test_get_login(self):
        #url = reverse("admin:index")
        #resp = self.client.get(url, follow=True)
        resp = self.client.get("/admin/login/", follow=True)
        self.assertRedirects(resp, '/fr/admin/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "admin/login.html")
        #self.assertIn("", resp.content)

    def test_post_login(self):
        self.client.login(**self.credentials)
        resp = self.client.post("/admin/login/", follow=True)
        self.assertRedirects(resp, '/fr/admin/login/')
        self.assertEqual(resp.status_code, 200)
        # should be logged in now, fails however
        self.assertTrue(resp.context['user'].is_active)
