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
#from api.models import Application
from api.models import Board
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from web.forms import UserProfileForm
from django.urls import reverse

from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


def main_site(request):
    t = get_template('main.html')
    #html = t.render(context={'boards': Board.objects.all().order_by('display_name'), 'applications': Application.objects.all().order_by('name'), 'modules': Module.objects.all().order_by('group_identifier')}, request=request)
    html = t.render(context={'boards': Board.objects.all().order_by('display_name'), 'applications': {}, 'modules': Module.objects.all().order_by('group_identifier')}, request=request)
    return HttpResponse(html)


@login_required
def user_profile(request):
    if(request.method == 'POST'):
        form = UserProfileForm(instance=request.user, data=request.POST)
        if(form.is_valid()):
            form.save()
        return HttpResponseRedirect(reverse('user-profile'))
    t = get_template('user_profile.html')
    form = UserProfileForm(instance=request.user)
    html = t.render(context={"form": form}, request=request)
    return HttpResponse(html)


def install_instruction_browser_integration(request):
    t = get_template('install_instruction_browser_integration.html')
    html = t.render()
    return HttpResponse(html)


#def generate_app_detail_view(template):
#
#    class AppDetails(DetailView):
#        model = Application
#        template_name = template
#
#    return AppDetails


#class AppInstall(DetailView):
#    model = Application
#    template_name = "app_build.html"
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["boards"] = Board.objects.all().order_by('display_name')
#        return context
