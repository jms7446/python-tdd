# from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
# import pytest

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


def test_home_page_returns_correct_html():
    request = HttpRequest()
    response = home_page(request)
    html = response.content.decode('utf8')
    assert html.startswith('<html>')
    assert '<title>To-Do lists</title>' in html
    assert html.endswith('</html>')
