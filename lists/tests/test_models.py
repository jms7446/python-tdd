import pytest

from django.core.exceptions import ValidationError

from lists.models import Item, List


def test_saving_and_retrieving_items():
    list_ = List.objects.create()
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


def test_cannot_save_empty_list_items():
    list_ = List.objects.create()
    item = Item(list=list_, text='')
    with pytest.raises(ValidationError):
        item.full_clean()
        item.save()
    assert Item.objects.count() == 0


def test_get_absolute_url():
    list_ = List.objects.create()
    assert list_.get_absolute_url() == f'/lists/{list_.id}/'
