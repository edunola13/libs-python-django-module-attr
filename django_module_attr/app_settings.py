# -*- coding: utf-8 -*-

from django.conf import settings

from rest_framework.permissions import IsAdminUser

MOD_ATTR = getattr(settings, 'DJ_MOD_ATTR', {})

PERMISSIONS = (MOD_ATTR.get('PERMISSIONS', None) or [IsAdminUser])
