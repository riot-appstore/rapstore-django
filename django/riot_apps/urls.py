"""riot_apps URL Configuratio2

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
from uploader.views import uploader
from django.contrib import admin

from django.conf.urls import url, include
from rest_framework import routers
from web.views import main_site, user_profile, install_instruction_browser_integration
from riot_apps import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from rest_framework.routers import DefaultRouter
from api.views import ApplicationViewSet

router = DefaultRouter()

router.register('apps', ApplicationViewSet, base_name='apps')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_site, name="main_site"),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^user-profile/', user_profile, {}, name='user-profile'),
    url(r'^uploader/', uploader, {}, name='uploader'),
    url(r'^api/', include(router.urls)),
    url(r'^install-instruction-browser-integration', install_instruction_browser_integration, {}, name='install-instruction-browser-integration')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
