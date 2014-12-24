#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.photo.views import home, home_files

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wappa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        home_files, name='home-files'),
)

    url(r'^admin/', include(admin.site.urls)),
)
