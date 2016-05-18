from django.conf.urls import url, include
from django.contrib import admin

from httpapi.views import httpapi_router
import legacy.urls as reporter

urlpatterns = [
    url(r'^old/', include(reporter.urls)),
    url(r'^api/v1/', include(httpapi_router.urls)),
    #url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^semirhage/', admin.site.urls),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^id/', include('allauth.urls')),
]