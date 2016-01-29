from django.contrib import admin

from core.models import Project, Progress


@admin.register(Progress, Project)
class SemirhageAdmin(admin.ModelAdmin):
    pass
