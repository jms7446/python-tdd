from selenium.webdriver.common.keys import Keys
from pytest import mark

from .conftest import *


def test_cannot_add_empty_list_items(browser, live_server_url):
    # Edith goes to the home page and accidentally try to submit an empty list item.
    # She hits Enter on the empty input box
    browser.get(live_server_url)
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys(Keys.ENTER)

    # The home page refreshes, and there is an error message saying that
    # list items cannot be blank
    elem = find_element_by_id_with_wait(browser, 'id_warning_msg')
    assert 'List items cannot be blank' in elem.text

    # She tries again with some text for the item, which now works
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('new item text')
    inputbox.send_keys(Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: new item text')

    # Perversely, she decides to submit a second blank list item
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    elem = find_element_by_id_with_wait(browser, 'id_warning_msg')
    assert 'List items cannot be blank' in elem.text

    # And she can correct it by filling some text in
    raise Exception('write me!')
