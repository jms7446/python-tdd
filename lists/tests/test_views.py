import pytest
from django.urls import resolve
from django.test import SimpleTestCase

from lists.views import home_page
from lists.models import Item, List


def assert_template_used(response, template_name):
    assert template_name in [t.name for t in response.templates]


################################################################################
# Homepage
################################################################################

def test_root_url_resolvers_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page


def test_uses_home_templates(client):
    response = client.get('/')
    assert_template_used(response, 'home.html')


################################################################################
# NewList
################################################################################

@pytest.mark.django_db
def test_can_save_a_post_request(client):
    client.post('/lists/new', data={'item_text': 'A new list item'})
    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new list item'


@pytest.mark.django_db
def test_redirects_after_post(client):
    item_text = 'A new list item'
    response = client.post('/lists/new', data={'item_text': item_text})
    new_list = List.objects.first()
    SimpleTestCase().assertRedirects(response, f'/lists/{new_list.id}/')


################################################################################
# NewItem
################################################################################

@pytest.mark.django_db
def test_can_save_a_post_request_to_an_existing_list(client):
    List.objects.create()
    correct_list = List.objects.create()

    client.post(
        f'/lists/{correct_list.id}/add_item',
        data={'item_text': 'A new item for an existing list'},
    )

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new item for an existing list'
    assert new_item.list == correct_list


@pytest.mark.django_db
def test_redirects_to_list_view(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f'/lists/{correct_list.id}/add_item',
        data={'item_text': 'A new item for an existing list'},
    )

    SimpleTestCase().assertRedirects(response, f'/lists/{correct_list.id}/')


################################################################################
# ListView
################################################################################

@pytest.mark.django_db
def test_uses_correct_template(client):
    List.objects.create()
    correct_list = List.objects.create()

    response = client.get(f'/lists/{correct_list.id}/')

    SimpleTestCase().assertTemplateUsed(response, 'list.html')


@pytest.mark.django_db
def test_passes_correct_list_to_template(client):
    _ = List.objects.create()
    correct_list = List.objects.create()

    response = client.get(f'/lists/{correct_list.id}/')

    assert response.context['list'] == correct_list


@pytest.mark.django_db
def test_displays_all_items(client):
    list_ = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_)
    Item.objects.create(text='itemey 2', list=list_)

    response = client.get(f'/lists/{list_.id}/')

    page_text = response.content.decode()
    assert 'itemey 1' in page_text
    assert 'itemey 2' in page_text
