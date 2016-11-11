from django.conf.urls import url

from dashboard import views

urls = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^my/profile$', views.profile, name='my_profile'),
    url(r'^people/(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^people$', views.list_users, name='list_users'),
    url(r'^projects$', views.list_projects, name='list_projects'),
    url(r'^projects\/(?P<id>\d+)$', views.project, name='project'),
    url(r'^deadlines$', views.list_deadlines, name='list_deadlines'),
    url(r'^deadlines\/(?P<id>\d+)$', views.deadline, name='deadline'),
    url(r'^year\/(?P<year>\d+)\/week\/(?P<week_label>\d+)\/summary$', views.week_summary, name='week_summary'),
    url(r'^chartsjs/week_chart.js$', views.time_comparison_bar_chart_data, name='week_chart_js'),
    url(r'^chartsjs/projects_chart.js$', views.projects_bar_chart_data, name='projects_chart_js'),
]