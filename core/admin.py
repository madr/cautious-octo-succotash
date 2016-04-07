from django.contrib import admin

from core.models import Project, Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['duration', 'note']
    list_filter = ['user']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['billable', 'name']
    list_filter = ['active', 'billable']

