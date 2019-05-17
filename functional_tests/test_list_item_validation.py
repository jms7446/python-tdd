from selenium.webdriver.common.keys import Keys

from .conftest import *


def test_cannot_add_empty_list_items(browser, live_server_url):
    # Edith goes to the home page and accidentally try to submit an empty list item.
    browser.get(live_server_url)

    # She hits Enter on the empty input box
    get_new_item_input_box(browser).send_keys(Keys.ENTER)

    # The home page refreshes, and there is an error message saying that
    # list items cannot be blank
    elem = wait_for(browser.find_element_by_css_selector, '.has-error', wait_time=1)
    assert "You can'n have an empty list item" in elem.text

    # She tries again with some text for the item, which now works
    get_new_item_input_box(browser).send_keys('Buy milk', Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: Buy milk')

    # Perversely, she decides to submit a second blank list item
    browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    elem = wait_for(browser.find_element_by_css_selector, '.has-error', wait_time=1)
    assert "You can'n have an empty list item" in elem.text

    # And she can correct it by filling some text in
    get_new_item_input_box(browser).send_keys('Make tea', Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: Buy milk')
    assert_text_in_table_rows_with_wait(browser, '2: Make tea')
