#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from apps.photo.forms import PhotoForm, PackForm

from apps.taxonomy.models import Status, Domain, Country, Gender
from apps.photo.models import Pack, PackTranslation, Photo
from django.core.paginator import Paginator, EmptyPage
from django.core.paginator import PageNotAnInteger

import hvad
from django.db.models import Q
from functools import reduce
from django.contrib.auth.models import Group, Permission, User
from django.core import urlresolvers
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

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


@login_required(login_url='/dashboard/login/')
def packs(request):
    lang = request.LANGUAGE_CODE # or django.utils.translation.get_language()
    stam = hvad.utils.get_translation_aware_manager(Status)
    dtam = hvad.utils.get_translation_aware_manager(Domain)
    ttam = hvad.utils.get_translation_aware_manager(Gender) #pack type

    status_list = [ s for s in stam.language(lang).all() ]
    domain_list = [ s for s in dtam.language(lang).all() ]
    type_list = [ s for s in ttam.language(lang).all() ]

    if 'is_modal' in request.GET and request.GET.get('is_modal') == '1':
        is_modal = True
    else:
        is_modal = False

    q = list()
    if request.GET.get('sn'):
        q.append(Q(status__id=request.GET.get('sn')))
    if request.GET.get('dn'):
        q.append(Q(domain__id=request.GET.get('dn')))
    if request.GET.get('tn'):
        q.append(Q(pack_type__id=request.GET.get('tn')))

    if q:
        pack_list = [ p for p in Pack.objects.language(lang).filter(reduce(lambda x,y: x and y, q)) ]
    else:
        pack_list = [ p for p in Pack.objects.language(lang).all() ]

    paginator = Paginator(pack_list, 10) # 10 packs per page
    page = request.GET.get('page')
    try:
        packs = paginator.page(page)
    except PageNotAnInteger:
        packs = paginator.page(1)
    except EmptyPage:
        packs = paginator.page(paginator.num_pages)
    template = 'photo/pack/list.html'

    return render(request, template,
                  {'packs': packs,
                   'is_modal': is_modal,
                   'statuses': status_list,
                   'domains': domain_list,
                  'types': type_list})


@login_required(login_url='/dashboard/login/')
def photos(request):
    lang = request.LANGUAGE_CODE # or django.utils.translation.get_language()
    stam = hvad.utils.get_translation_aware_manager(Status)

    status_list = [ s for s in stam.language(lang).all() ]
    user_list = [ u for u in User.objects.all() ]

    if 'is_modal' in request.GET and request.GET.get('is_modal') == '1':
        is_modal = True
    else:
        is_modal = False

    q = list()
    if request.GET.get('sn'):
        q.append(Q(status__id=request.GET.get('sn')))
    if request.GET.get('un'):
        q.append(Q(author__id=request.GET.get('dn')))

    if q:
        photo_list = [ p for p in Photo.objects.filter(reduce(lambda x,y: x and y, q)) ]
    else:
        photo_list = [ p for p in Photo.objects.all() ]

    paginator = Paginator(photo_list, 10) # 10 photos per page
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    template = 'photo/photo/list.html'
    return render(request, template,
                  {'photos': photos,
                   'is_modal': is_modal,
                   'users': user_list,
                  'statuses': status_list})

@csrf_protect
@login_required(login_url='/dashboard/login/')
def add_pack(request, id=None):
    template = 'photo/pack/form.html'
    if id:
        pack = get_object_or_404(Pack, pk=id)
        pack_photos = pack.photos.values_list('id')
        edit = True
        message = _('Pack successfully updated.')
    else:
        pack = Pack()
        edit = False
        message = _('Pack successfully added.')

    if request.method == 'POST':
        form = PackForm(request.POST, instance=pack)

        # ugly and probably dangerous hack
        photos = form.data.get('photos', '')
        photos = photos.strip('[]')
        photos = "".join(photos.split())
        photos = photos.split(',')
        form.data['photos'] = photos

        if form.is_valid():
            pack = form.save(commit=False)
            if not id: pack.save()
            pack_en = PackTranslation.objects.get_or_create(master_id=pack.id,
                                                            language_code='en')
            pack_en[0].title=form.cleaned_data.get('title_en','')
            pack_en[0].description=form.cleaned_data.get('description_en','')
            pack_en[0].save()

            pack_fr = PackTranslation.objects.get_or_create(master_id=pack.id,
                                                            language_code='fr')
            pack_fr[0].title=form.cleaned_data.get('title_fr','')
            pack_fr[0].description=form.cleaned_data.get('description_fr','')
            pack_fr[0].save()
            form.save_m2m()

            messages.add_message(request, messages.INFO, message)
            return HttpResponseRedirect(urlresolvers.reverse('dashboard:packs'))
    else:
        form = PackForm(instance=pack)
    return render(request, template,
                  {'form': form,
                   'edit': edit})


@csrf_protect
@login_required(login_url='/dashboard/login/')
def add_photo(request, id=None):
    template = 'photo/photo/form.html'
    if id:
        photo = get_object_or_404(Photo, pk=id)
        edit = True
        message = _('Photo successfully updated.')
        # if photo.author != request.user:
        #     return HttpResponseForbidden()
    else:
        photo = Photo(author=request.user)
        edit = False
        message = _('Photo successfully added.')

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            # process data if necessary
            # save
            form.save()
            #
            messages.add_message(request, messages.INFO, message)
            # redirect
            return HttpResponseRedirect(urlresolvers.reverse('dashboard:photos'))
    else:
        form = PhotoForm(instance=photo)
    return render(request, template,
                  {'form': form,
                   'edit': edit})
