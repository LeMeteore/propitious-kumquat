#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import password_reset
from django.contrib.auth.views import password_reset_done
from django.contrib.auth.views import password_reset_confirm
from django.contrib.auth.views import password_reset_complete
from django.contrib.auth.views import password_change
from django.contrib.auth.views import password_change_done

from . import dashboard_views as views


urlpatterns = patterns(
    '',
    url(r'^$', views.dashboard, name='dashboard_index'),
    url(r'^login/$', views.login, name='dashboard_login'),
    url(r'^logout/$', views.logout, name='dashboard_logout'),
)


# password related stuff
urlpatterns += patterns(
    url(r'^password/done/$', password_reset_complete),

    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect' : '/password/done/'}),

    url(r'^password/reset/$', password_reset,
        {'template_name':'photo/registration/password_reset_form.html',
         'email_template_name': 'photo/registration/password_reset_email.html',
        'subject_template_name': 'photo/registration/password_reset_subject.txt',},
        name='dashboard_password_reset'),

    url(r'^password/change/$', password_change,
        {'template_name': 'photo/registration/password_change_form.html',
         'post_change_redirect': 'dashboard_password_change_done'},
        name='dashboard_password_change'),

    url(r'^password/reset/done/$',
        password_reset_done,
        name='dashboard_password_reset_done'),

    url(r'^password/change/done/$',
        password_change_done,
        {'template_name':'photo/registration/password_change_done.html',},
        name='dashboard_password_change_done'),

)
