# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

"""riot_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from api.views import ApplicationViewSet
from api.views import ApplicationInstanceViewSet
from api.views import BoardViewSet
from api.views import BuildManagerViewSet
from api.views import UserViewSet
from api.views import FeedbackViewSet
from api.views import SecureSocialLogin
from api.views import get_social
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'app', ApplicationViewSet, base_name='application')
router.register(r'instance', ApplicationInstanceViewSet, base_name='instance')
router.register(r'board', BoardViewSet)
router.register(r'user', UserViewSet, base_name='user')
router.register(r'feedback', FeedbackViewSet)
router.register(r'buildmanager', BuildManagerViewSet, base_name='buildmanager')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^api/', include(router.urls)),
    url(r'^social/login/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        SecureSocialLogin.as_view(), name='social_token_user'),
    url(r'^social/url/(?:(?P<provider>[a-zA-Z0-9_-]+)/?)?$',
        get_social, name='social_url'),
]
