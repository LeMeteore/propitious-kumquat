#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.simple_tag
def is_active(request, pattern):
    if pattern in request.path:
        return 'active'
    return ''

@register.simple_tag
def is_active_reverse(request, urlname):
    if reverse(urlname) in request.path:
        return 'active'
    return ''
