# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Category, Tag

from .serializers import (
    CategorySerializer, TagSerializer
)


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.filter(enabled=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = self.get_queryset().order_by('name')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.filter(enabled=True)
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = self.get_queryset().order_by('name')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
