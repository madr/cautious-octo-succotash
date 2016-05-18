#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Project, AbsenceCategory, Progress


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'date_joined', 'first_name',
                   'last_name', 'groups', 'user_permissions')


class AbsentiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceCategory


class ProgressSerializer(serializers.ModelSerializer):
    included_serializers = {
        'project': ProjectSerializer,
        'user': UserSerializer,
    }

    class Meta:
        model = Progress


class AbsenceSerializer(serializers.ModelSerializer):
    included_serializers = {
        'absentia': AbsentiaSerializer,
        'user': UserSerializer,
    }

    class Meta:
        model = Progress


class WhoAmISerializer(serializers.Serializer):
    email = serializers.EmailField()
    login = serializers.CharField()
    name = serializers.CharField()