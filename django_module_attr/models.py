# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models


class Category (models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True)
    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag (models.Model):
    name = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)


class GenericData(models.Model):
    value = models.TextField()

    def get_value(self):
        try:
            return json.loads(self.value)
        except Exception:
            return None
