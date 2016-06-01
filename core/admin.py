from django.contrib import admin

from core.models import Project, Progress, Absence, AbsenceCategory


def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


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
    list_display = ['note', 'project', 'duration', 'done_at']
    list_filter = ['user']
    search_fields = ['note', 'project']


@admin.register(Absence)
class AbsenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'duration', 'done_at']
    list_filter = ['user']
    search_fields = ['note']


@admin.register(Absence)
class AbsenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'duration', 'done_at']
    list_filter = ['category', 'user']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'billable', 'active']
    list_filter = ['active', 'billable']
    search_fields = ['name']
    actions = [make_active, make_not_active, make_billable, make_not_billable]


@admin.register(AbsenceCategory)
class AbsentiaAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    list_filter = ['active']
    search_fields = ['name']
    actions = [make_active, make_not_active]
