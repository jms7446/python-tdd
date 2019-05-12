import time

from selenium.webdriver.common.keys import Keys
from pytest import fixture

from util import make_driver


@fixture
def browser():
    browser = make_driver('chrome')
    yield browser
    browser.quit()


def test_can_start_a_list_and_retrieve_it_later(browser):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser.get('http://localhost:8000')

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

    table = browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    assert any(row.text == '1: Buy peacock feathers' for row in rows), "New to-do item did not appear in table"

    # There is still a text box inviting her to add another item.
    # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
    raise Exception('Finish the test!')

    # The page updates again, and now shows both items on her list

    # Edith wonders whether the site will remember her list. Then she sees
    # that the site has generated a unique URL for her -- there is some
    # explanatory text to that effect.

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep
