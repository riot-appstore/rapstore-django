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
from api.views import request_download
from django.contrib import admin

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
from api.views import ApplicationViewSet
from api.views import BoardViewSet
from web.views import main_site, user_profile, install_instruction_browser_integration
from web.views import main_site
from web.views import user_profile
from web.views import generate_app_detail_view
from web.views import AppInstall
from riot_apps import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout
from django.contrib.auth.views import login

router = routers.DefaultRouter()
router.register(r'app', ApplicationViewSet)
router.register(r'board', BoardViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^$', main_site, name="main_site"),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^build/$', request_download, {}, name='build'),
    url(r'^user-profile/', user_profile, {}, name='user-profile'),
    url(r'^install-instruction-browser-integration', install_instruction_browser_integration, {}, name='install-instruction-browser-integration'),
    url(r'^app_details/(?P<pk>\d+)/$', generate_app_detail_view(template="app_detail.html").as_view(), {}, name='app-details'),
    url(r'^app_details/(?P<pk>\d+)/install/$', AppInstall.as_view(), {}, name='app-install'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
