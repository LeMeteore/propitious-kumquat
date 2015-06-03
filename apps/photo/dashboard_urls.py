#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from . import dashboard_views as views


urlpatterns = patterns(
    '',
    url(r'^$', views.dashboard, name='dashboard_index'),
    url(r'^login/$', views.login, name='dashboard_login'),
)
