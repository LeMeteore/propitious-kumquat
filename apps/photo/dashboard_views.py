#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url='/dashboard/login/')
def dashboard(request):
    #return HttpResponse("this is the dashboard")
    return render(request, 'photo/dashboard.html')

@csrf_protect
def login(request, authentication_form=AuthenticationForm,):
    if request.method == 'POST':
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())
            return HttpResponseRedirect('/dashboard/')
    else:
        form = AuthenticationForm()
    return render(request, 'photo/registration/login.html',
                  {'user_form': form})

def logout(request, template_name="photo/registration/logged_out.html"):
    auth_logout(request)
    return TemplateResponse(request, template_name)
