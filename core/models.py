import datetime

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from rest_framework.compat import MinValueValidator


def validate_duration(value):
    if value % 15 != 0:
        raise serializers.ValidationError('only even quarters allowed, for example: 15, 45, 180, 105')


class Project(models.Model):
    name = models.CharField(max_length=128)
    billable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "projects"

    class JSONAPIMeta:
        resource_name = "projects"

    def user_set(self):
        users = list(set([p.user_id for p in self.progress_set.all()]))
        user_set = TajmUser.objects.filter(pk__in=users)
        return user_set


class TajmUser(User):
    class Meta:
        proxy = True

    def project_set(self):
        projects = list(set([p.project_id for p in self.progress_set.all()]))
        project_set = Project.objects.filter(pk__in=projects)
        return project_set


class Progress(models.Model):
    user = models.ForeignKey(TajmUser)
    duration = models.IntegerField(default=15, validators=[MinValueValidator(15), validate_duration])
    note = models.TextField()
    done_at = models.DateField(default=datetime.date.today)
    created_at = models.DateField(auto_now_add=True)
    started_at = models.TimeField(default='00:00:00')

    project = models.ForeignKey(Project, null=True)

    def __str__(self):
        return self.note

    class Meta:
        ordering = ["-done_at", 'created_at']
        verbose_name_plural = "progresses"

    class JSONAPIMeta:
        resource_name = "progresses"


class AbsenceCategory(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    class JSONAPIMeta:
        resource_name = "absence_categories"


class Absence(models.Model):
    user = models.ForeignKey(TajmUser)
    duration = models.IntegerField(default=480, validators=[MinValueValidator(15), validate_duration])
    note = models.TextField(default='', blank=True)
    done_at = models.DateField(default=datetime.date.today)
    started_at = models.TimeField(default='00:00:00')
    created_at = models.DateField(auto_now_add=True)

    category = models.ForeignKey(AbsenceCategory, null=True)

    def __str__(self):
        return self.category.name

    class Meta:
        ordering = ["-done_at"]
        verbose_name_plural = "absences"

    class JSONAPIMeta:
        resource_name = "absences"
