#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_files(request, filename):
    return render(request,
                  filename,
                  {},
                  content_type="text/plain")

def home(request):
    return HttpResponse("hello world")
