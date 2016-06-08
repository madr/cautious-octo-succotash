from django.contrib import admin
from django.http import HttpResponseRedirect

from core.models import Project, Progress, Absence, AbsenceCategory


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


def merge_projects(modeladmin, request, queryset):
    new_project = Project(name='(merged %d projects)' % queryset.count())
    new_project.save()

    for project in queryset.all():
        Progress.objects.filter(project=project).update(project=new_project)
        project.delete()

    return HttpResponseRedirect("%d/change/" % new_project.pk)


def make_not_active(modeladmin, request, queryset):
    queryset.update(active=False)


def make_billable(modeladmin, request, queryset):
    queryset.update(billable=True)


def make_not_billable(modeladmin, request, queryset):
    queryset.update(billable=False)


make_active.short_description = "Mark selected as active"
make_not_active.short_description = "Mark selected as not active"
make_billable.short_description = "Mark selected as billable"
make_not_billable.short_description = "Mark selected as not billable"


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['note', 'duration', 'done_at', 'user', 'project']
    list_filter = ['user']
    search_fields = ['note', 'project__name']


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ['category', 'duration', 'done_at']
    list_filter = ['category', 'user']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'billable', 'active']
    list_filter = ['active', 'billable']
    search_fields = ['name']
    actions = [make_active, make_not_active, make_billable, make_not_billable, merge_projects]


@admin.register(AbsenceCategory)
class AbsenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    list_filter = ['active']
    search_fields = ['name']
    actions = [make_active, make_not_active]
