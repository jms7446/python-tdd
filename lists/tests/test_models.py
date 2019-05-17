import pytest

from lists.models import Item, List


################################################################################
# ItemModel
################################################################################

@pytest.mark.django_db
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
