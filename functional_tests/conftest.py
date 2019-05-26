import os
import time
from functools import wraps

from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, get_user_model
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome
from pytest import fixture

from util import make_driver

MAX_WAIT = 2
WAIT_INTERVAL = 0.2

User = get_user_model()


def wait_for(func, *args, wait_time=MAX_WAIT, wait_interval=WAIT_INTERVAL, **kwargs):
    start_time = time.time()
    while True:
        try:
            return func(*args, **kwargs)
        except (AssertionError, WebDriverException):
            if time.time() - start_time < wait_time:
                time.sleep(wait_interval)
            else:
                raise


def wait(d_func=None, wait_time=MAX_WAIT, wait_interval=WAIT_INTERVAL):
    def wait2(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            wait_for(func, *args, wait_time=wait_time, wait_interval=wait_interval, **kwargs)
        return decorated_func

    if callable(d_func):
        # direct decorator
        return wait2(d_func)
    else:
        return wait2


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


@wait
def assert_text_in_table_rows_with_wait(browser, row_text):
    table = browser.find_element_by_id('id_list_table')
    assert_text_in_table_rows(table, row_text)


def assert_text_in_table_rows(table_elem, row_text):
    rows = table_elem.find_elements_by_tag_name('tr')
    assert row_text in [row.text for row in rows]


def find_item_input_box(browser: Chrome):
    return browser.find_element_by_id('id_text')


def create_pre_authenticated_session(email, browser, server_url):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    ## to set a cookie we need to first visit the domain.
    ## 404 pages load the quickest!
    browser.get(server_url + "/404_no_such_url/")
    browser.add_cookie(dict(
        name=settings.SESSION_COOKIE_NAME,
        value=session.session_key,
        path='/',
    ))


@wait(wait_time=3)
def wait_to_be_logged_in(browser, email):
    browser.find_element_by_link_text('Log out')
    navbar = browser.find_element_by_css_selector('.navbar')
    assert email in navbar.text


@wait
def wait_to_be_logged_out(browser, email):
    browser.find_element_by_name('email')
    navbar = browser.find_element_by_css_selector('.navbar')
    assert email not in navbar.text
