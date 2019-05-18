from selenium.webdriver.common.keys import Keys

from .conftest import *


def test_cannot_add_empty_list_items(browser, live_server_url):
    # Edith goes to the home page and accidentally try to submit an empty list item.
    browser.get(live_server_url)

    # She hits Enter on the empty input box
    find_item_input_box(browser).send_keys(Keys.ENTER)

    # The browser intercepts the request, and does not load the list page
    wait_for(browser.find_element_by_css_selector, '#id_text:invalid')

    # She tries again with some text for the item, which now works
    find_item_input_box(browser).send_keys('Buy milk')
    wait_for(browser.find_element_by_css_selector, '#id_text:valid')

    find_item_input_box(browser).send_keys(Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: Buy milk')

    # Perversely, she decides to submit a second blank list item
    find_item_input_box(browser).send_keys(Keys.ENTER)

    # Again, the browser will not comply
    assert_text_in_table_rows_with_wait(browser, '1: Buy milk')
    wait_for(browser.find_element_by_css_selector, '#id_text:invalid')

    # And she can correct it by filling some text in
    find_item_input_box(browser).send_keys('Make tea')
    wait_for(browser.find_element_by_css_selector, '#id_text:valid')
    find_item_input_box(browser).send_keys(Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: Buy milk')
    assert_text_in_table_rows_with_wait(browser, '2: Make tea')


def test_cannot_add_duplicate_items(browser, live_server_url):
    # Edith goes to the home page and starts a new list
    browser.get(live_server_url)
    find_item_input_box(browser).send_keys('Buy wellies', Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: Buy wellies')

    # She accidentally tries to enter a duplicate item
    find_item_input_box(browser).send_keys('Buy wellies', Keys.ENTER)

    # She sees a helpful error message
    elem = wait_for(browser.find_element_by_css_selector, '.has-error')
    assert elem.text == "You've already got this in your list"



