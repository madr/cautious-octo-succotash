from django.contrib import admin

from core.models import Project, Progress, Customer


@admin.register(Customer, Progress, Project)
class SemirhageAdmin(admin.ModelAdmin):
    pass
