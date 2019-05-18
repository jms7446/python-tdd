import pytest

from django.core.exceptions import ValidationError

from lists.models import Item, List


@pytest.fixture
def list_():
    return List.objects.create()


def test_default_text():
    item = Item()
    assert item.text == ''


def test_item_is_related_to_list(list_):
    item = Item()
    item.list = list_
    item.save()
    assert item in list_.item_set.all()


def test_list_ordering(list_):
    item1 = Item.objects.create(list=list_, text='i1')
    item2 = Item.objects.create(list=list_, text='item 2')
    item3 = Item.objects.create(list=list_, text='3')
    item4 = Item.objects.create(list=list_, text='2')
    item5 = Item.objects.create(list=list_, text='1')

    assert list(Item.objects.all()) == [item1, item2, item3, item4, item5]


def test_string_representation():
    item = Item(text='some text')
    assert str(item) == 'some text'


def test_cannot_save_empty_list_items(list_):
    item = Item(list=list_, text='')
    with pytest.raises(ValidationError):
        item.full_clean()
        item.save()
    assert Item.objects.count() == 0


def test_get_absolute_url(list_):
    assert list_.get_absolute_url() == f'/lists/{list_.id}/'


def test_duplicate_items_are_invalid(list_):
    Item.objects.create(list=list_, text='bla')
    with pytest.raises(ValidationError):
        item = Item(list=list_, text='bla')
        item.full_clean()
        item.save()


def test_can_save_same_item_to_different_lists():
    list1 = List.objects.create()
    list2 = List.objects.create()
    Item.objects.create(list=list1, text='bla')
    item = Item(list=list2, text='bla')
    item.full_clean()       # should not raise
