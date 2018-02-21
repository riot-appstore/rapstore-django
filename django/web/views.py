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
from django.http import HttpResponseRedirect
from api.models import Module
from api.models import Application
from api.models import Board
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from web.forms import UserProfileForm
from django.urls import reverse


def main_site(request):
    t = get_template('main.html')
    html = t.render(context={'boards': Board.objects.all().order_by('display_name'), 'applications': Application.objects.all().order_by('name'), 'modules': Module.objects.all().order_by('group_identifier')}, request=request)
    return HttpResponse(html)

def user_profile(request):
    if(request.method == 'POST'):
        form = UserProfileForm(instance=request.user, data=request.POST)
        if(form.is_valid()):
            form.save()
        return HttpResponseRedirect(reverse('user-profile'))
    t = get_template('user_profile.html')
    form = UserProfileForm({"email": request.user.email})
    html = t.render(context={"form": form}, request=request)
    return HttpResponse(html)
