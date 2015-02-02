#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from apps.taxonomy.models import Country, Domain, Status, Gender
from hvad.admin import TranslatableAdmin
from django.utils.translation import ugettext_lazy as _


class CountryModelAdmin(TranslatableAdmin):
    # add_form_template = "admin/taxonomy/add_country_form.html"
    # change_form_template = "admin/taxonomy/change_country_form.html"
    # change_list_template = "admin/taxonomy/change_country_list.html"
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    pass

class DomainModelAdmin(TranslatableAdmin):
    # add_form_template = "admin/taxonomy/add_domain_form.html"
    # change_form_template = "admin/taxonomy/change_domain_form.html"
    # change_list_template = "admin/taxonomy/change_domain_list.html"
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    pass

class StatusModelAdmin(TranslatableAdmin):
    # add_form_template = "admin/taxonomy/add_status_form.html"
    # change_form_template = "admin/taxonomy/change_status_form.html"
    # change_list_template = "admin/taxonomy/change_status_list.html"
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    pass

class GenderModelAdmin(TranslatableAdmin):
    # add_form_template = "admin/taxonomy/add_type_form.html"
    # change_form_template = "admin/taxonomy/change_type_form.html"
    # change_list_template = "admin/taxonomy/change_type_list.html"
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    pass

admin.site.register(Gender, GenderModelAdmin)
admin.site.register(Domain, DomainModelAdmin)
admin.site.register(Status, StatusModelAdmin)
admin.site.register(Country, CountryModelAdmin)
