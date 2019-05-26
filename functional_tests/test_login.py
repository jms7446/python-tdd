import re

from selenium.webdriver.common.keys import Keys
from django.core import mail

from .conftest import *

TEST_EMAIL = 'jms7446@hanmail.net'
SUBJECT = 'Your login link for Superlists'


def test_can_get_email_link_to_log_in(browser, live_server_url):
    # Edith goes to the awesome superlists site and notices a "Log in" section in the
    # navbar for the first time
    # It's telling her to enter her email address, so she does
    browser.get(live_server_url)
    browser.find_element_by_name('email').send_keys(TEST_EMAIL, Keys.ENTER)

    # A message appears telling her an email has been sent
    elem = wait_for(browser.find_element_by_tag_name, 'body')
    assert 'Check your email' in elem.text

    # She checks her email and finds a message
    email = mail.outbox[0]
    assert TEST_EMAIL in email.to
    assert email.subject == SUBJECT

    # It has a url link in it
    assert 'Use this link to log in' in email.body
    url_search = re.search(r'http://.+/.+$', email.body)
    assert url_search
    url = url_search.group(0)
    assert live_server_url in url

    # she clicks it
    browser.get(url)

    # she is logged in!
    wait_to_be_logged_in(browser, TEST_EMAIL)

    # Now she logs out
    browser.find_element_by_link_text('Log out').click()

    # She is logged out
    wait_to_be_logged_out(browser, TEST_EMAIL)
