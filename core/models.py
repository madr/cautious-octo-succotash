import datetime
from django.contrib.auth.models import User, Group
from django.db import models


class Customer(models.Model):
    def trial_expires_date():
        return datetime.date.today() + datetime.timedelta(days=60)

    name = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField()
    active = models.BooleanField(default=True)
    trial = models.BooleanField(default=False)
    trial_expires_at = models.DateField(default=trial_expires_date)
    group = models.ForeignKey(Group)
    deactivated_users = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.note

    class Meta:
        ordering = ["active", "name"]
        verbose_name_plural = "customers"


class Project(models.Model):
    customer = models.ForeignKey(Customer)
    name = models.CharField(max_length=128)
    billable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("customer", "name")
        ordering = ["name"]
        verbose_name_plural = "projects"


class Progress(models.Model):
    customer = models.ForeignKey(Customer)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    duration = models.IntegerField(default=15)
    note = models.TextField()
    done_at = models.DateField(default=datetime.date.today)
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.note

    class Meta:
        ordering = ["-done_at"]
        verbose_name_plural = "progresses"
