import os
import django
import pytest

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.api.settings')
    django.setup() 