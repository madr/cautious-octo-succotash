from django.conf.urls import url

from dashboard import views

urls = [
    url(r'^$', views.dashboard, name='dashboard'),
]