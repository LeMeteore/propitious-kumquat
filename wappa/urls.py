#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from apps.photo.views import home, home_files

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        home_files, name='home-files'),
)

urlpatterns += i18n_patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('apps.photo.dashboard_urls')),
    url(r'^$', home, name='home'),
)

if settings.DEBUG == True:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
