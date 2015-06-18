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
    url(r'^$', views.dashboard, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
)


# password related stuff
urlpatterns += patterns(
    '',
    url(r'^password/reset/$', password_reset,
        {'template_name':'photo/registration/password_reset_form.html',
         'email_template_name': 'photo/registration/password_reset_email.html',
         'subject_template_name': 'photo/registration/password_reset_subject.txt',
         'post_reset_redirect':'dashboard:password_reset_done',},
        name='password_reset'),

    url(r'^password/reset/done/$', password_reset_done,
        {'template_name': 'photo/registration/password_reset_done.html',},
        name='password_reset_done'),

    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'photo/registration/password_reset_confirm.html',
         'post_reset_redirect' : 'dashboard:password_done'},
        name='password_reset_confirm'),

    url(r'^password/change/$', password_change,
        {'template_name': 'photo/registration/password_change_form.html',
         'post_change_redirect': 'dashboard:password_change_done'},
        name='password_change'),

    url(r'^password/change/done/$',
        password_change_done,
        {'template_name':'photo/registration/password_change_done.html',},
        name='password_change_done'),

    url(r'^password/done/$', password_reset_complete,
        {'template_name':'photo/registration/password_reset_complete.html'},
        name='password_done'),

)
