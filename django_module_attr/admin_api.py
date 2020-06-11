# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from django_module_attr import app_settings

from .models import (
    Category, Tag
)

from .serializers import (
    AdminCategorySerializer,
    AdminTagSerializer
)


class AdminCategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = app_settings.PERMISSIONS

    __basic_fields = ('name',)
    filter_fields = __basic_fields + ('enabled',)
    search_fields = __basic_fields
    ordering_fields = __basic_fields
    ordering = 'name'


class AdminTagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = AdminTagSerializer
    permission_classes = app_settings.PERMISSIONS

    __basic_fields = ('name',)
    filter_fields = __basic_fields + ('enabled',)
    search_fields = __basic_fields
    ordering_fields = __basic_fields
    ordering = 'name'
