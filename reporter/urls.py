from django.conf.urls import patterns, url
import reporter.views as reporter_views

urls = [
    url(r'^projects.js$', reporter_views.projects, name='projects.js'),
    url(r'^$', reporter_views.report, name='today'),
    url(r'^absence/(?P<absence_id>\d+)/delete$', reporter_views.delete_absence, name='delete_absence'),
    url(r'^year\/(?P<year>\d+)\/week\/(?P<week_label>\d+)\/day\/(?P<day>\d+)$', reporter_views.report, name='anyday'),
    url(r'^year\/(?P<year>\d+)\/week\/(?P<week_label>\d+)\/day\/(?P<day>\d+)\/progress\/(?P<progress_id>\d+)/edit$', reporter_views.edit_progress, name='edit_progress'),
    url(r'^year\/(?P<year>\d+)\/week\/(?P<week_label>\d+)\/day\/(?P<day>\d+)\/progress\/(?P<progress_id>\d+)/delete$', reporter_views.delete_progress, name='delete_progress'),
]