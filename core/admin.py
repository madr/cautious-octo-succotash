from django.contrib import admin

from core.models import Project, Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['note', 'duration']
    list_filter = ['user']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'billable']
    list_filter = ['active', 'billable']

