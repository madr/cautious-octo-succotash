from django.conf.urls import url, include
from django.contrib import admin, auth

import tajm.dashboard.urls as dashboard
from tajm.httpapi.views import httpapi_router

urlpatterns = [
    url(r'^api/v1/', include(httpapi_router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^id/logout/$', auth.views.logout, {'next_page': '/'}),
    url(r'^id/', include('allauth.urls')),
    url(r'^', include(dashboard.urls)),
]

admin.site.site_header = 'Tajm admin'
