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

def names(t):
    class AdminClass(admin.ModelAdmin):
        list_display=t
    return AdminClass

# Register your models here.
admin.site.register(Board, names(('internal_name',)))
admin.site.register(Application, names(('name', 'description')))
admin.site.register(ApplicationInstance, names(('application', 'is_public')))
admin.site.register(Module, names(('name', 'description')))
admin.site.register(Transaction, names(('uuid',)))
admin.site.register(Feedback, names(('date', 'description',)))
admin.site.register(UserProfile)
