import pytest
from django.urls import resolve
from django.test import SimpleTestCase
import django

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


@pytest.mark.django_db
def test_only_saves_items_when_necessary(client):
    client.get('/')
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_uses_home_templates(client):
    response = client.get('/')
    assert_template_used(response, 'home.html')


################################################################################
# NewList
################################################################################

@pytest.mark.django_db
def test_can_save_a_post_request(client):
    item_text = 'A new list item'
    _ = client.post('/lists/new', data={'item_text': item_text})
    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == item_text


@pytest.mark.django_db
def test_redirects_after_post(client):
    item_text = 'A new list item'
    response = client.post('/lists/new', data={'item_text': item_text})
    new_list = List.objects.first()
    SimpleTestCase().assertRedirects(response, f'/lists/{new_list.id}/')


################################################################################
# NewList
################################################################################

@pytest.mark.django_db
def test_can_save_a_post_request_to_an_existing_list(client):
    other_list = List.objects.create()
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
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = client.post(
        f'/lists/{correct_list.id}/add_item',
        data={'item_text': 'A new item for an existing list'},
    )

    SimpleTestCase().assertRedirects(response, f'/lists/{correct_list.id}/')


################################################################################
# ItemModel
################################################################################

@pytest.mark.django_db
def test_saving_and_retrieving_items():
    list_ = List()
    list_.save()

    first_item = Item()
    first_text = 'The first (ever) list item'
    first_item.text = first_text
    first_item.list = list_
    first_item.save()

    second_item = Item()
    second_text = 'Item the second'
    second_item.text = second_text
    second_item.list = list_
    second_item.save()

    saved_list = List.objects.first()
    assert saved_list == list_

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == first_text
    assert first_saved_item.list == list_
    assert second_saved_item.text == second_text
    assert second_saved_item.list == list_


################################################################################
# ListView
################################################################################

@pytest.mark.django_db
def test_passes_correct_list_to_template(client):
    _ = List.objects.create()
    correct_list = List.objects.create()
    response = client.get(f'/lists/{correct_list.id}/')
    SimpleTestCase().assertTemplateUsed(response, 'list.html')


@pytest.mark.django_db
def test_displays_all_items(client):
    list_ = List.objects.create()
    Item.objects.create(text='itemey 1', list=list_)
    Item.objects.create(text='itemey 2', list=list_)

    response = client.get(f'/lists/{list_.id}/')

    page_text = response.content.decode()
    assert 'itemey 1' in page_text
    assert 'itemey 2' in page_text


@pytest.mark.django_db
def test_passes_correct_list_to_template(client):
    _ = List.objects.create()
    correct_list = List.objects.create()
    response = client.get(f'/lists/{correct_list.id}/')
    assert response.context['list'] == correct_list
