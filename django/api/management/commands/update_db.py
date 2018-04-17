# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from django.core.management.base import BaseCommand
from api.models import Transaction


def update_riot_apps():
    pass


class Command(BaseCommand):
    help = 'Populate Boards, Modules, Apps with RIOT'

    def handle(self, *args, **options):
        transaction = Transaction.objects.create()
        try:
            update_riot_apps()
            print('OK')

        except Exception as e:
            transaction.delete()
            print('FAIL: {}'.format(str(e)))
