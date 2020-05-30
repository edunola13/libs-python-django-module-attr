# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from mock import patch

from django.urls import reverse
from rest_framework import status

from .test import APITestCase

from django_module_attr.models import Category, Tag


class CategoryApiTests(APITestCase):

    def setUp(self):
        self.user = self.user_factory.create(is_staff=True, password="123456")
        self.client = self.client_class()
        self.client.login(username=self.user.username, password="123456")

        self.category_1 = Category.objects.create(
            name="Nombre 1",
            description="",
            enabled=True
        )
        self.category_2 = Category.objects.create(
            name="Nombre 2",
            description="Descripcion 2",
            enabled=True
        )
        self.category_3 = Category.objects.create(
            name="Nombre 3",
            description="",
            enabled=True
        )
        self.category_4 = Category.objects.create(
            name="Nombre 4",
            description="",
            enabled=False
        )

    def test_list(self):
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(len(data), 3)

        data_cat = data[0]

        # Check received fields
        self.assertTrue('id' in data_cat)
        self.assertTrue('name' in data_cat)
        self.assertTrue('description' in data_cat)
        self.assertTrue('enabled' not in data_cat)
        self.assertTrue('created_at' not in data_cat)
        self.assertTrue('updated_at' not in data_cat)

        category = Category.objects.get(pk=data_cat.get('id'))
        self.assertEqual(data_cat['name'], category.name)
        self.assertEqual(data_cat['description'], category.description)

    def test_get(self):
        url = reverse('categories-detail', kwargs={'pk': self.category_1.id})

        # Default
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data_cat = response.json()

        self.assertTrue('id' in data_cat)
        self.assertTrue('name' in data_cat)
        self.assertTrue('description' in data_cat)
        self.assertTrue('enabled' not in data_cat)
        self.assertTrue('created_at' not in data_cat)
        self.assertTrue('updated_at' not in data_cat)

        self.assertEqual(data_cat['name'], self.category_1.name)
        self.assertEqual(data_cat['description'], self.category_1.description)

    def test_get_not_found(self):
        url = reverse('categories-detail', kwargs={'pk': self.category_4.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagApiTests(APITestCase):

    def setUp(self):
        self.user = self.user_factory.create(is_staff=True, password="123456")
        self.client = self.client_class()
        self.client.login(username=self.user.username, password="123456")

        self.tag_1 = Tag.objects.create(
            name="Nombre 1",
            enabled=True
        )
        self.tag_2 = Tag.objects.create(
            name="Nombre 2",
            enabled=True
        )
        self.tag_3 = Tag.objects.create(
            name="Nombre 3",
            enabled=True
        )
        self.tag_4 = Tag.objects.create(
            name="Nombre 4",
            enabled=False
        )

    def test_list(self):
        url = reverse('tags-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(len(data), 3)

        data_tag = data[0]

        # Check received fields
        self.assertTrue('id' in data_tag)
        self.assertTrue('name' in data_tag)
        self.assertTrue('enabled' not in data_tag)
        self.assertTrue('created_at' not in data_tag)
        self.assertTrue('updated_at' not in data_tag)

        tag = Tag.objects.get(pk=data_tag.get('id'))
        self.assertEqual(data_tag['name'], tag.name)

    def test_get(self):
        url = reverse('tags-detail', kwargs={'pk': self.tag_1.id})

        # Default
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data_tag = response.json()

        self.assertTrue('id' in data_tag)
        self.assertTrue('name' in data_tag)
        self.assertTrue('enabled' not in data_tag)
        self.assertTrue('created_at' not in data_tag)
        self.assertTrue('updated_at' not in data_tag)

        self.assertEqual(data_tag['name'], self.tag_1.name)

    def test_get_not_found(self):
        url = reverse('tags-detail', kwargs={'pk': self.tag_4.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
