import pytest
from django.urls import resolve
from django.test import SimpleTestCase
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


################################################################################
# Homepage
################################################################################

def test_root_url_resolvers_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page


def test_uses_home_templates(client, test_case):
    response = client.get('/')
    test_case.assertTemplateUsed(response, 'home.html')


def test_home_page_uses_item_form(client):
    response = client.get('/')
    assert isinstance(response.context['form'], ItemForm)


################################################################################
# NewList
################################################################################

def test_can_save_a_post_request(client):
    client.post('/lists/new', data={'text': 'A new list item'})
    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new list item'


def test_redirects_after_post(client, test_case):
    text = 'A new list item'
    response = client.post('/lists/new', data={'text': text})
    new_list = List.objects.first()
    test_case.assertRedirects(response, f'/lists/{new_list.id}/')


def test_for_invalid_input_renders_home_template(client, test_case):
    response = client.post('/lists/new', data={'text': ''})
    assert response.status_code == 200
    test_case.assertTemplateUsed(response, 'home.html')


def test_validation_errors_are_shown_on_home_page(client, test_case):
    response = client.post('/lists/new', data={'text': ''})
    expected_error = escape(EMPTY_ITEM_ERROR)
    test_case.assertContains(response, expected_error)


def test_for_invalid_input_passes_form_to_template(client, test_case):
    response = client.post('/lists/new', data={'text': ''})
    assert isinstance(response.context['form'], ItemForm)


def test_invalid_list_items_are_not_saved(client):
    client.post('/lists/new', data={'text': ''})

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
        data={'text': 'A new item for an existing list'},
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
        data={'text': 'A new item for an existing list'},
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


def test_displays_item_form(client, test_case):
    list_ = List.objects.create()
    response = client.get(f'/lists/{list_.id}/')
    assert isinstance(response.context['form'], ItemForm)
    test_case.assertContains(response, 'name="text"')


def test_validation_errors_end_up_on_lists_page(client, test_case):
    list_ = List.objects.create()
    response = client.post(f'/lists/{list_.id}/', data={'text': ''})

    assert response.status_code == 200
    assert test_case.assertTemplateUsed('list.html')
    test_case.assertContains(response, escape("You can't have an empty list item"))


def post_invalid_input_to_list_view(client):
    list_ = List.objects.create()
    response = client.post(f'/lists/{list_.id}/', data={'text': ''})
    return response


def test_for_invalid_input_nothing_saved_to_db(client):
    post_invalid_input_to_list_view(client)
    assert Item.objects.count() == 0


def test_for_invalid_input_renders_list_template(client, test_case):
    response = post_invalid_input_to_list_view(client)
    assert response.status_code == 200
    test_case.assertTemplateUsed(response, 'list.html')


def test_for_invalid_input_passes_form_to_template_in_item_list(client):
    response = post_invalid_input_to_list_view(client)
    assert isinstance(response.context['form'], ItemForm)


def test_for_invalid_input_shows_error_on_page(client, test_case):
    response = post_invalid_input_to_list_view(client)
    test_case.assertContains(response, escape(EMPTY_ITEM_ERROR))


@pytest.mark.skip
def test_duplicate_item_validation_errors_end_up_on_lists_page(client):
    list_ = List.objects.create()
    Item.objects.create(list=list_, text='textey')
    response = client.post(f'/lists/{list_.id}/', data={'text': 'textey'})

    SimpleTestCase().assertContains(response, escape("You've already got this in your list"))
    SimpleTestCase().assertTemplateUsed(response, 'list.html')
    assert Item.objects.count() == 1
