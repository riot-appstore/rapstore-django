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

class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'download', 
        'publish'
    )

    def download(self, obj):
        instance = obj.applicationinstance_set.first()
        return format_html('<a class="button" href="{}"> Download </a>'.format(reverse('application-download', args=[obj.pk])))

    def publish(self, obj):
        instance = obj.applicationinstance_set.first()
        html = format_html('<a class="button" href="{}"> Publish </a>'.format(""))
        return html if not instance.is_public else ""

# Register your models here.
admin.site.register(Board, names(('internal_name',)))
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationInstance, names(('application', 'is_public')))
admin.site.register(Module, names(('name', 'description')))
admin.site.register(Transaction, names(('uuid',)))
admin.site.register(Feedback, names(('date', 'description',)))
admin.site.register(UserProfile)
