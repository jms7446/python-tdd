import pytest
from django.urls import resolve

from lists.views import home_page
from lists.models import Item


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
    assert response.status_code == 302
    assert response['location'] == '/lists/one-list/'


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


################################################################################
# ListView
################################################################################

@pytest.mark.django_db
def test_uses_list_template(client):
    response = client.get('/lists/one-list/')
    assert_template_used(response, 'list.html')


@pytest.mark.django_db
def test_displays_all_items(client):
    Item.objects.create(text='itemey 1')
    Item.objects.create(text='itemey 2')

    response = client.get('/lists/one-list/')

    page_text = response.content.decode()
    assert 'itemey 1' in page_text
    assert 'itemey 2' in page_text
