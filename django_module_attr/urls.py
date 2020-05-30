# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.routers import DefaultRouter

from .api import (
    CategoryViewSet, TagViewSet
)
from .admin_api import (
    AdminCategoryViewSet, AdminTagViewSet
)

router = DefaultRouter()
# Public Section
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'categories', CategoryViewSet, basename='categories')
# Admin Section
router.register(r'admin/categories', AdminCategoryViewSet, basename='admin-categories')
router.register(r'admin/tags', AdminTagViewSet, basename='admin-tags')

urlpatterns = [
]

urlpatterns += router.urls
