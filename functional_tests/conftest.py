import os

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
    table = find_element_by_id_with_wait(browser, 'id_list_table', MAX_WAIT)
    rows = table.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]
