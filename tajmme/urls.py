from django.conf.urls import url, include
from django.contrib import admin
import dashboard.urls as dashboard

from httpapi.views import httpapi_router
import reporter.urls as reporter

urlpatterns = [
    url(r'^reporter/', include(reporter.urls)),
    url(r'^api/v1/', include(httpapi_router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^id/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^id/', include('allauth.urls')),
    url(r'^', include(dashboard.urls)),
]
