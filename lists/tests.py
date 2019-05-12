import pytest
from pytest_django import plugin
# from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

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


def test_uses_home_templates(client):
    response = client.get('/')
    assert 'home.html' in (t.name for t in response.templates)


def test_home_page_returns_correct_html():
    request = HttpRequest()
    response = home_page(request)
    html = response.content.decode('utf8')
    expected_html = render_to_string('home.html')
    assert html == expected_html
