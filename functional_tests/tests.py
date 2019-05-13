import time
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from pytest import fixture

from util import make_driver

MAX_WAIT = 3


@fixture
def browser():
    browser = make_driver('chrome')
    yield browser
    browser.quit()


def find_element_by_id_with_wait(browser, elem_id, wait):
    elem = WebDriverWait(browser, wait).until(
        ec.presence_of_element_located((By.ID, elem_id))
    )
    return elem


def assert_text_in_table_rows(browser, row_text):
    table = find_element_by_id_with_wait(browser, 'id_list_table', MAX_WAIT)
    rows = table.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]


def test_can_start_a_list_for_one_user(browser, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get(live_server.url)

    # she notices the page title and header mention to-do lists
    print(browser.title)
    assert 'To-Do' in browser.title
    header_text = browser.find_element_by_tag_name('h1').text
    assert 'To-Do' in header_text

    # She is invited to enter a to-do item straight away
    input_box = browser.find_element_by_id('id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

    # She types "Buy peacock feathers" into a text box
    # (Edith's hobby is tying fly-fishing lures)
    input_box.send_keys('Buy peacock feathers')

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    input_box.send_keys(Keys.ENTER)

    # assert any(row.text == '1: Buy peacock feathers' for row in rows), f"contents: {table.text}"
    assert_text_in_table_rows(browser, '1: Buy peacock feathers')

    # There is still a text box inviting her to add another item.
    # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('Use peacock feathers to make a fly')
    input_box.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    assert_text_in_table_rows(browser, '1: Buy peacock feathers')
    assert_text_in_table_rows(browser, '2: Use peacock feathers to make a fly')

    # Satisfied, she goes back to sleep


def test_multiple_users_can_start_lists_at_different_urls(browser, live_server):
    # Edith starts a new to-do list
    # browser = make_driver()
    browser.get(live_server.url)
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('Buy peacock feathers')
    input_box.send_keys(Keys.ENTER)
    assert_text_in_table_rows(browser, '1: Buy peacock feathers')

    # She notices that her list has a unique URL
    edith_list_url = browser.current_url
    assert re.findall('/lists/.+', edith_list_url)

    # Now a new user, Francis, comes along to the site.

    ## We use a new browser session to make sure that no information
    ## of Edith's is coming through from cookies etc
    browser.delete_all_cookies()

    # Francis visits the home page. There is no sign of Edith's list
    browser.get(live_server.url)
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'make a fly' not in page_text

    # Francis starts a new list by entering a new item.
    # He is less interesting than Edith...
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('Buy milk')
    input_box.send_keys(Keys.ENTER)
    assert_text_in_table_rows(browser, '1: Buy milk')

    # Francis gets his own unique URL
    francis_list_url = browser.current_url
    assert re.findall('/lists/.+', francis_list_url)
    assert francis_list_url != edith_list_url

    # Again, there is no trace of Edith's list
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'Buy milk' in page_text

    # Satisfied, they both go back to sleep
