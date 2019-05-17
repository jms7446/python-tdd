import pytest
from django.urls import resolve
from django.test import SimpleTestCase
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List


################################################################################
# Homepage
################################################################################

def test_root_url_resolvers_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page


def test_uses_home_templates(client, test_case):
    response = client.get('/')
    test_case.assertTemplateUsed(response, 'home.html')


################################################################################
# NewList
################################################################################

def test_can_save_a_post_request(client):
    client.post('/lists/new', data={'item_text': 'A new list item'})
    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new list item'


def test_redirects_after_post(client, test_case):
    item_text = 'A new list item'
    response = client.post('/lists/new', data={'item_text': item_text})
    new_list = List.objects.first()
    test_case.assertRedirects(response, f'/lists/{new_list.id}/')


def test_validation_errors_are_sent_back_to_home_page_template(client, test_case):
    response = client.post('/lists/new', data={'item_text': ''})

    assert response.status_code == 200
    test_case.assertTemplateUsed(response, 'home.html')
    expected_error = escape("You can't have an empty list item")
    test_case.assertContains(response, expected_error)


def test_invalid_list_items_are_not_saved(client):
    client.post('/lists/new', data={'item_text': ''})

    assert List.objects.count() == 0
    assert Item.objects.count() == 0


################################################################################
# NewItem
################################################################################

def test_can_save_a_post_request_to_an_existing_list(client):
    List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f'/lists/{correct_list.id}/',
        data={'item_text': 'A new item for an existing list'},
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new item for an existing list'
    assert new_item.list == correct_list


def test_POST_redirects_to_list_view(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f'/lists/{correct_list.id}/',
        data={'item_text': 'A new item for an existing list'},
    )

    SimpleTestCase().assertRedirects(response, f'/lists/{correct_list.id}/')


################################################################################
# ListView
################################################################################

def test_uses_correct_template(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.get(f'/lists/{correct_list.id}/')

    SimpleTestCase().assertTemplateUsed(response, 'list.html')


def test_passes_correct_list_to_template(client):
    _ = List.objects.create()
    correct_list = List.objects.create()

    response = client.get(f'/lists/{correct_list.id}/')

    assert response.context['list'] == correct_list


def test_displays_all_items(client):
    list_ = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_)
    Item.objects.create(text='itemey 2', list=list_)

    response = client.get(f'/lists/{list_.id}/')

    page_text = response.content.decode()
    assert 'itemey 1' in page_text
    assert 'itemey 2' in page_text
