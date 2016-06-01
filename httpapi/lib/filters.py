#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import rest_framework_filters as filters
from core.models import Project, AbsenceCategory, Progress, Absence


class UserFilter(filters.FilterSet):
    class Meta:
        model = User


class AbsenceCategoryFilter(filters.FilterSet):
    name = filters.AllLookupsFilter()

    created_at = filters.DateFilter()
    created__gte = filters.DateFilter(name='created_at', lookup_expr='gte')
    created__lte = filters.DateFilter(name='created_at', lookup_expr='lte')
    created__gt = filters.DateFilter(name='created_at', lookup_expr='gt')
    created__lt = filters.DateFilter(name='created_at', lookup_expr='lt')

    billable = filters.BooleanFilter()
    active = filters.BooleanFilter()

    class Meta:
        model = AbsenceCategory


class ProjectFilter(AbsenceCategoryFilter):
    billable = filters.BooleanFilter()

    class Meta:
        model = Project


class ProgressFilter(filters.FilterSet):
    done_at = filters.DateFilter()
    done_at__gte = filters.DateFilter(name='done_at', lookup_expr='gte')
    done_at__lte = filters.DateFilter(name='done_at', lookup_expr='lte')
    done_at__gt = filters.DateFilter(name='done_at', lookup_expr='gt')
    done_at__lt = filters.DateFilter(name='done_at', lookup_expr='lt')

    created_at = filters.DateFilter()
    created__gte = filters.DateFilter(name='created_at', lookup_expr='gte')
    created__lte = filters.DateFilter(name='created_at', lookup_expr='lte')
    created__gt = filters.DateFilter(name='created_at', lookup_expr='gt')
    created__lt = filters.DateFilter(name='created_at', lookup_expr='lt')

    note = filters.AllLookupsFilter()

    project = filters.RelatedFilter(ProjectFilter, name='project')
    user = filters.RelatedFilter(UserFilter, name='user')

    class Meta:
        model = Progress


class AbsenceFilter(ProgressFilter):
    class Meta:
        model = Absence
