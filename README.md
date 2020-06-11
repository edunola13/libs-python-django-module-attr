=====
Module Attributes
=====

Module Attributes is a Django app for basic functionallity of Attributes.

Quick start
-----------

1. Add "django_module_attr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
    	'django_module_attr',
    ]

2. Include the module attr URLconf in your project urls.py like this::

    path('attr/', include('django_module_attr.urls')),

Or add the custom rule like you wish.

3. Add the next settings:
    - DJ_MOD_ATTR: Module attr specific settings:
        - PERMISSIONS: Permissions for admin api.

4. Run ``python manage.py migrate`` to create the users models.


=====
Developers Module
=====

You need develop your module like any django app. After that you need a test_settings because there is no django_project y run makemigrations y tests with this settings. Fot that we use the edited manage.py

Steps after development:
 - python manage.py makemigrations
 - python manage.py test
