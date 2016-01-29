from django.conf.urls import url, include
from django.contrib import admin

from httpapi.views import httpapi_router

urlpatterns = [
    url(r'^api/v1/', include(httpapi_router.urls)),
    url(r'^semirhage/', admin.site.urls),
    url(r'^id/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
