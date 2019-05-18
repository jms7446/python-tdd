import os
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import Chrome
from pytest import fixture

from util import make_driver

MAX_WAIT = 1


@fixture
def browser():
    browser = make_driver('chrome')
    yield browser
    browser.quit()


@fixture
def live_server_url(live_server):
    staging_server = os.environ.get('STAGING_SERVER')
    if staging_server:
        url = 'http://' + staging_server
    else:
        url = live_server.url
    yield url


def find_element_by_id_with_wait(browser, elem_id, wait=MAX_WAIT):
    elem = WebDriverWait(browser, wait).until(
        ec.presence_of_element_located((By.ID, elem_id))
    )
    return elem


def assert_text_in_table_rows_with_wait(browser, row_text):
    table = wait_for(browser.find_element_by_id, 'id_list_table')
    assert_text_in_table_rows(table, row_text)


def assert_text_in_table_rows(table_elem, row_text):
    rows = table_elem.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]


def wait_for(func, *args, wait_time=MAX_WAIT, **kwargs):
    start_time = time.time()
    while True:
        try:
            return func(*args, **kwargs)
        except (AssertionError, WebDriverException):
            if time.time() - start_time < wait_time:
                time.sleep(0.1)
            else:
                raise


def find_item_input_box(browser):
    return browser.find_element_by_id('id_text')
