"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from django.shortcuts import render
import textwrap
from django.http import HttpResponse
from api.models import Module
from api.models import Application
from api.models import Board
from django.template.loader import get_template
from django.template import RequestContext

def main_site(request):
    t = get_template('main.html')
    html = t.render(context={'boards': Board.objects.all(), 'applications': Application.objects.all(), 'modules': Module.objects.all().order_by('group_identifier')}, request=request)
    return HttpResponse(html)
