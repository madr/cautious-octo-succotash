import datetime

from django.contrib.auth.models import User, Group
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


class Progress(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    duration = models.IntegerField(default=15, validators=[MinValueValidator(15), validate_duration])
    note = models.TextField()
    done_at = models.DateField(default=datetime.date.today)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        ordering = ["-done_at"]
        verbose_name_plural = "progresses"
