# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from mock import patch

from django.urls import reverse
from rest_framework import status

from .test import APITestCase

from django_module_attr.models import Category, Tag


class CategoryAdminApiTests(APITestCase):

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
        url = reverse('admin-categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data['count'], 4)
        self.assertEqual(data['previous'], None)
        self.assertEqual(data['next'], None)
        self.assertEqual(len(data['results']), 4)

        # Filter enabled
        response = self.client.get(url + "?enabled=0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['previous'], None)
        self.assertEqual(data['next'], None)
        self.assertEqual(len(data['results']), 1)

        data_cat = data['results'][0]

        # Check received fields
        self.assertTrue('id' in data_cat)
        self.assertTrue('name' in data_cat)
        self.assertTrue('description' in data_cat)
        self.assertTrue('enabled' in data_cat)
        self.assertTrue('created_at' in data_cat)
        self.assertTrue('updated_at' in data_cat)

        category = Category.objects.get(pk=data_cat.get('id'))
        self.assertEqual(data_cat['name'], category.name)
        self.assertEqual(data_cat['description'], category.description)
        self.assertEqual(data_cat['enabled'], category.enabled)
        self.assertEqual(data_cat['created_at'], category.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_cat['updated_at'], category.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_list_no_permission(self):
        """
            Works for every endpoint
        """
        url = reverse('admin-categories-list')

        self.user.is_staff = False
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        url = reverse('admin-categories-detail', kwargs={'pk': self.category_1.id})

        # Default
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data_cat = response.json()

        self.assertTrue('id' in data_cat)
        self.assertTrue('name' in data_cat)
        self.assertTrue('description' in data_cat)
        self.assertTrue('enabled' in data_cat)
        self.assertTrue('created_at' in data_cat)
        self.assertTrue('updated_at' in data_cat)

        self.assertEqual(data_cat['name'], self.category_1.name)
        self.assertEqual(data_cat['description'], self.category_1.description)
        self.assertEqual(data_cat['enabled'], self.category_1.enabled)
        self.assertEqual(data_cat['created_at'], self.category_1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_cat['updated_at'], self.category_1.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_get_not_found(self):
        url = reverse('admin-categories-detail', kwargs={'pk': 0})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        url = reverse('admin-categories-list')

        data = {
            'name': 'New Category',
            'description': 'La Descripcion',
            'enabled': True
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_cat = response.json()

        # Check received fields
        self.assertTrue('id' in data_cat)
        self.assertTrue('name' in data_cat)
        self.assertTrue('description' in data_cat)
        self.assertTrue('enabled' in data_cat)
        self.assertTrue('created_at' in data_cat)
        self.assertTrue('updated_at' in data_cat)

        category = Category.objects.get(pk=data_cat.get('id'))
        self.assertEqual(data_cat['name'], category.name)
        self.assertEqual(data_cat['description'], category.description)
        self.assertEqual(data_cat['enabled'], category.enabled)
        self.assertEqual(data_cat['created_at'], category.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_cat['updated_at'], category.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_create_validation(self):
        url = reverse('admin-categories-list')

        data = {'description': '', 'enabled': None}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_validation = response.json()
        self.assertEqual(data_validation['enabled'], ['This field may not be null.'])
        self.assertEqual(data_validation['name'], ['This field is required.'])

        data = {'name': 'Nombre 1', 'description': ''}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_validation = response.json()
        self.assertEqual(data_validation['name'], ['category with this name already exists.'])

    def test_update(self):
        url = reverse('admin-categories-detail', kwargs={'pk': self.category_2.id})

        data = {
            'name': 'Nombre 2 Update',
            'enabled': False
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_cat = response.json()

        # Check received fields
        self.assertTrue('id' in data_cat)
        self.assertTrue('name' in data_cat)
        self.assertTrue('description' in data_cat)
        self.assertTrue('enabled' in data_cat)
        self.assertTrue('created_at' in data_cat)
        self.assertTrue('updated_at' in data_cat)

        category = Category.objects.get(pk=data_cat.get('id'))
        self.assertEqual(data_cat['description'], category.description)
        self.assertEqual(data_cat['name'], category.name)
        self.assertEqual(data_cat['name'], data['name'])
        self.assertEqual(data_cat['enabled'], category.enabled)
        self.assertEqual(data_cat['enabled'], data['enabled'])
        self.assertEqual(data_cat['created_at'], category.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_cat['updated_at'], category.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_update_validation(self):
        url = reverse('admin-categories-detail', kwargs={'pk': self.category_2.id})

        data = {'name': None}
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_validation = response.data
        self.assertEqual(data_validation['name'], ['This field may not be null.'])

    def test_update_not_found(self):
        url = reverse('admin-categories-detail', kwargs={'pk': 0})

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        url = reverse('admin-categories-detail', kwargs={'pk': self.category_3.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_found(self):
        url = reverse('admin-categories-detail', kwargs={'pk': 0})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagAdminApiTests(APITestCase):

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
        url = reverse('admin-tags-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data['count'], 4)
        self.assertEqual(data['previous'], None)
        self.assertEqual(data['next'], None)
        self.assertEqual(len(data['results']), 4)

        # Filter enabled
        response = self.client.get(url + "?enabled=0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['previous'], None)
        self.assertEqual(data['next'], None)
        self.assertEqual(len(data['results']), 1)

        data_tag = data['results'][0]

        # Check received fields
        self.assertTrue('id' in data_tag)
        self.assertTrue('name' in data_tag)
        self.assertTrue('enabled' in data_tag)
        self.assertTrue('created_at' in data_tag)
        self.assertTrue('updated_at' in data_tag)

        tag = Tag.objects.get(pk=data_tag.get('id'))
        self.assertEqual(data_tag['name'], tag.name)
        self.assertEqual(data_tag['enabled'], tag.enabled)
        self.assertEqual(data_tag['created_at'], tag.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_tag['updated_at'], tag.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_list_no_permission(self):
        """
            Works for every endpoint
        """
        url = reverse('admin-tags-list')

        self.user.is_staff = False
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        url = reverse('admin-tags-detail', kwargs={'pk': self.tag_1.id})

        # Default
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data_tag = response.json()

        self.assertTrue('id' in data_tag)
        self.assertTrue('name' in data_tag)
        self.assertTrue('enabled' in data_tag)
        self.assertTrue('created_at' in data_tag)
        self.assertTrue('updated_at' in data_tag)

        self.assertEqual(data_tag['name'], self.tag_1.name)
        self.assertEqual(data_tag['enabled'], self.tag_1.enabled)
        self.assertEqual(data_tag['created_at'], self.tag_1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_tag['updated_at'], self.tag_1.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_get_not_found(self):
        url = reverse('admin-tags-detail', kwargs={'pk': 0})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        url = reverse('admin-tags-list')

        data = {
            'name': 'New Tag',
            'enabled': True
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_tag = response.json()

        # Check received fields
        self.assertTrue('id' in data_tag)
        self.assertTrue('name' in data_tag)
        self.assertTrue('enabled' in data_tag)
        self.assertTrue('created_at' in data_tag)
        self.assertTrue('updated_at' in data_tag)

        tag = Tag.objects.get(pk=data_tag.get('id'))
        self.assertEqual(data_tag['name'], tag.name)
        self.assertEqual(data_tag['enabled'], tag.enabled)
        self.assertEqual(data_tag['created_at'], tag.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_tag['updated_at'], tag.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_create_validation(self):
        url = reverse('admin-tags-list')

        data = {'description': '', 'enabled': None}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_validation = response.json()
        self.assertEqual(data_validation['enabled'], ['This field may not be null.'])
        self.assertEqual(data_validation['name'], ['This field is required.'])

        data = {'name': 'Nombre 1'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_validation = response.json()
        self.assertEqual(data_validation['name'], ['tag with this name already exists.'])

    def test_update(self):
        url = reverse('admin-tags-detail', kwargs={'pk': self.tag_2.id})

        data = {
            'name': 'Nombre 2 Update',
            'enabled': False
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_tag = response.json()

        # Check received fields
        self.assertTrue('id' in data_tag)
        self.assertTrue('name' in data_tag)
        self.assertTrue('enabled' in data_tag)
        self.assertTrue('created_at' in data_tag)
        self.assertTrue('updated_at' in data_tag)

        tag = Tag.objects.get(pk=data_tag.get('id'))
        self.assertEqual(data_tag['name'], tag.name)
        self.assertEqual(data_tag['name'], data['name'])
        self.assertEqual(data_tag['enabled'], tag.enabled)
        self.assertEqual(data_tag['enabled'], data['enabled'])
        self.assertEqual(data_tag['created_at'], tag.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data_tag['updated_at'], tag.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def test_update_validation(self):
        url = reverse('admin-tags-detail', kwargs={'pk': self.tag_2.id})

        data = {'name': None}
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data_validation = response.data
        self.assertEqual(data_validation['name'], ['This field may not be null.'])

    def test_update_not_found(self):
        url = reverse('admin-tags-detail', kwargs={'pk': 0})

        response = self.client.put(url, data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        url = reverse('admin-tags-detail', kwargs={'pk': self.tag_3.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_found(self):
        url = reverse('admin-tags-detail', kwargs={'pk': 0})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
