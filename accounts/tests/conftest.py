from django.test import SimpleTestCase
import pytest


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """enable django db access in this tests"""


@pytest.fixture
def test_case():
    """Django TestCase for using methods"""
    return SimpleTestCase()
