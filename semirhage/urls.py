from django.conf.urls import url, include
from django.contrib import admin
import dashboard.urls as dashboard

from httpapi.views import httpapi_router
import legacy.urls as legacy_reporter

urlpatterns = [
    url(r'^old/', include(legacy_reporter.urls)),
    url(r'^api/v1/', include(httpapi_router.urls)),
    # todo: fix and re-enable, does not work with https
    # url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^semirhage/', admin.site.urls),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^id/', include('allauth.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^', include(dashboard.urls)),
]
