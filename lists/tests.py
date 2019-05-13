import pytest
from pytest_django import plugin
# from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


# class SmokeTest(TestCase):
#
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)


def is_template_used(response, template_name):
    return template_name in (t.name for t in response.templates)


################################################################################
# Homepage
################################################################################

def test_root_url_resolvers_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page


def test_uses_home_templates(client):
    response = client.get('/')
    assert is_template_used(response, 'home.html')


def test_can_save_a_post_request(client):
    item_text = 'A new list item'
    response = client.post('/', data={'item_text': item_text})
    assert item_text in response.content.decode()
    assert is_template_used(response, 'home.html')


################################################################################
# ItemModel
################################################################################

@pytest.mark.django_db
def test_saving_and_retrieving_items():
    first_item = Item()
    first_text = 'The first (ever) list item'
    first_item.text = first_text
    first_item.save()

    second_item = Item()
    second_text = 'Item the second'
    second_item.text = second_text
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == first_text
    assert second_saved_item.text == second_text
