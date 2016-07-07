from django.conf.urls import url

from dashboard import views
from dashboard.forms import ProgressSearchForm
from dashboard.views import ProgressSearchView

urls = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^search/$', ProgressSearchView(form_class=ProgressSearchForm), name='search_progresses'),
]