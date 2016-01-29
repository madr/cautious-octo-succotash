import datetime
from django.contrib.auth.models import User, Group
from django.db import models


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

    duration = models.IntegerField(default=15)
    note = models.TextField()
    done_at = models.DateField(default=datetime.date.today)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.note

    class Meta:
        ordering = ["-done_at"]
        verbose_name_plural = "progresses"
