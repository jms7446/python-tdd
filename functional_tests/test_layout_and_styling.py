from selenium.webdriver.common.keys import Keys
from pytest import approx

from .conftest import *


def test_layout_and_styling(browser, live_server_url):
    # Edith goes to the home page
    browser.get(live_server_url)
    browser.set_window_size(1024, 768)

    # She notices the input box is nicely centered
    inputbox = find_item_input_box(browser)
    assert inputbox.location['x'] + inputbox.size['width'] / 2 == approx(512, abs=10)

    # She starts a new list and sees the input is nicely centered there too
    inputbox.send_keys('testing')
    inputbox.send_keys(Keys.ENTER)
    assert_text_in_table_rows_with_wait(browser, '1: testing')
    inputbox = find_item_input_box(browser)
    assert inputbox.location['x'] + inputbox.size['width'] / 2 == approx(512, abs=10)
