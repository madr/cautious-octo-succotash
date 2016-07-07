from django.contrib import admin
from django.http import HttpResponseRedirect

from core.models import Project, Progress, Absence, AbsenceCategory


def convert_projects_to_absence_category(modeladmin, request, queryset):
    # todo: write unit tests
    new_ac = AbsenceCategory(name='(converted from %d projects)' % queryset.count())
    new_ac.save()

    for project in queryset.all():
        progresses = Progress.objects.filter(project=project)

        for p in progresses:
            absence = Absence(category=new_ac, duration=p.duration, done_at=p.done_at, note=p.note, user=p.user)
            absence.save()

        progresses.delete()
        project.delete()

    return HttpResponseRedirect('../absencecategory/%d/change/' % new_ac.pk)


def merge_projects(modeladmin, request, queryset):
    # todo: write unit tests
    new_project = Project(name='(merged %d projects)' % queryset.count())
    new_project.save()

    for project in queryset.all():
        Progress.objects.filter(project=project).update(project=new_project)
        project.delete()

    return HttpResponseRedirect('%d/change/' % new_project.pk)


def merge_absence_categories(modeladmin, request, queryset):
    # todo: write unit tests
    new_ac = AbsenceCategory(name='(merged %d absence categories)' % queryset.count())
    new_ac.save()

    for ac in queryset.all():
        Absence.objects.filter(category=ac).update(category=new_ac)
        ac.delete()

    return HttpResponseRedirect('%d/change/' % new_ac.pk)


def make_active(modeladmin, request, queryset):
    # todo: write unit tests
    queryset.update(active=True)


def make_not_active(modeladmin, request, queryset):
    # todo: write unit tests
    queryset.update(active=False)


def make_billable(modeladmin, request, queryset):
    # todo: write unit tests
    queryset.update(billable=True)


def make_not_billable(modeladmin, request, queryset):
    # todo: write unit tests
    queryset.update(billable=False)


make_active.short_description = 'Mark selected as active'
make_billable.short_description = 'Mark selected as billable'
make_not_active.short_description = 'Mark selected as not active'
make_not_billable.short_description = 'Mark selected as not billable'
merge_absence_categories.short_description = 'Merge selected to new absence category'
merge_projects.short_description = 'Merge selected to new project'
convert_projects_to_absence_category.short_description = 'Convert selected projects to Absences'


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['note', 'duration', 'done_at', 'user', 'project']
    list_filter = ['user']
    search_fields = ['note', 'project__name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'billable', 'active', 'created_at']
    list_filter = ['active', 'billable']
    search_fields = ['name']
    actions = [make_active, make_not_active, make_billable, make_not_billable, merge_projects,
               convert_projects_to_absence_category]


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ['category', 'duration', 'user', 'done_at']
    list_filter = ['category', 'user']


@admin.register(AbsenceCategory)
class AbsenceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    list_filter = ['active']
    search_fields = ['name']
    actions = [make_active, make_not_active, merge_absence_categories]
