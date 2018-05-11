# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from django.contrib import admin
from api.models import Board
from api.models import Application
from api.models import ApplicationInstance
from api.models import Module
from api.models import Transaction
from api.models import UserProfile
from api.models import Feedback
from django.utils.html import format_html
from rest_framework.reverse import reverse


def names(t):
    class AdminClass(admin.ModelAdmin):
        list_display=t
    return AdminClass


def make_approved(modeladmin, request, queryset):
    for q in queryset:
        q.applicationinstance_set.update(is_public=True)


def make_unpublish(modeladmin, request, queryset):
    for q in queryset:
        q.applicationinstance_set.update(is_public=False)


make_approved.short_description = "Approve selected apps"
make_unpublish.short_description = "Unpublish selected apps"


class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'download',
        'approve'
    )
    actions = [make_approved, make_unpublish]

    def download(self, obj):
        instance = obj.applicationinstance_set.first()
        return format_html('<a class="button" href="{}"> Download </a>'.format(reverse('application-download', args=[obj.pk])))

    def approve(self, obj):
        instance = obj.applicationinstance_set.first()
        return instance.is_public

    approve.boolean=True

# Register your models here.
admin.site.register(Board, names(('internal_name',)))
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationInstance, names(('application', 'version_code', 'version_name',)))
admin.site.register(Module, names(('name', 'description')))
admin.site.register(Transaction, names(('uuid',)))
admin.site.register(Feedback, names(('date', 'description',)))
admin.site.register(UserProfile)
