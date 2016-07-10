from django.conf.urls import url

from dashboard import views
from dashboard.forms import ProgressSearchForm
from dashboard.views import ProgressSearchView

urls = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^chart-data/bar-chart.js$', views.time_comparison_bar_chart_data, name='bar_chart_data'),
    url(r'^chart-data/horizontal-bar-chart.js$', views.projects_bar_chart_data, name='hbar_chart_data'),
    url(r'^search/$', ProgressSearchView(form_class=ProgressSearchForm), name='search_progresses'),
]