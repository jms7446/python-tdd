import time

from selenium.webdriver.common.keys import Keys
from pytest import fixture

from util import make_driver


@fixture
def browser():
    browser = make_driver('chrome')
    yield browser
    browser.quit()


def assert_text_in_table_rows(browser, row_text):
    table = browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]


def test_can_start_a_list_and_retrieve_it_later(browser, live_server):
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
    time.sleep(1)

    # assert any(row.text == '1: Buy peacock feathers' for row in rows), f"contents: {table.text}"
    assert_text_in_table_rows(browser, '1: Buy peacock feathers')

    # There is still a text box inviting her to add another item.
    # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('Use peacock feathers to make a fly')
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    # The page updates again, and now shows both items on her list
    assert_text_in_table_rows(browser, '1: Buy peacock feathers')
    assert_text_in_table_rows(browser, '2: Use peacock feathers to make a fly')

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.
    raise Exception('Finish the test!')

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep
