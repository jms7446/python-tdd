# from django.test import TestCase
from django.urls import resolve
import pytest

from lists.views import home_page


# class SmokeTest(TestCase):
#
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)


################################################################################
# Homepage
################################################################################

def test_root_url_resolvers_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page
