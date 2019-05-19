import pytest

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import List, Item


################################################################################
# ItemForm
################################################################################

def test_form_item_input_has_placeholder_and_css_classes():
    form = ItemForm()
    assert 'placeholder="Enter a to-do item"' in form.as_p()
    assert 'class="form-control input-lg"' in form.as_p()


def test_form_validation_for_blank_items():
    form = ItemForm(data={'text': ''})
    assert not form.is_valid()
    assert form.errors['text'] == [EMPTY_ITEM_ERROR]


def test_form_save_handles_saving_to_a_list():
    list_ = List.objects.create()
    form = ItemForm(data={'text': 'do me'})
    new_item = form.save(for_list=list_)

    assert new_item == Item.objects.first()
    assert new_item.text == 'do me'
    assert new_item.list == list_


################################################################################
# ExistingListItemForm
################################################################################

def test_for_existing_list_form_renders_item_text_input():
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_)
    assert 'placeholder="Enter a to-do item"' in form.as_p()


def test_for_existing_list_form_validation_for_blank_items():
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_, data={'text': ''})
    assert not form.is_valid()
    assert form.errors['text'] == [EMPTY_ITEM_ERROR]


def test_for_existing_list_form_save_handles_saving_to_a_list():
    list_ = List.objects.create()
    Item.objects.create(list=list_, text='no twins!')
    form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})

    assert not form.is_valid()
    assert form.errors['text'] == [DUPLICATE_ITEM_ERROR]
