import re
import os
import poplib

from selenium.webdriver.common.keys import Keys
from django.core import mail

from .conftest import *

TEST_EMAIL = 'jms7446.app@gmail.com'
SUBJECT = 'Your login link for Superlists'


def test_can_get_email_link_to_log_in(browser, live_server_url):
    ## for new mail check, we make checker before server send mail
    mail_checker = MailChecker()

    # Edith goes to the awesome superlists site and notices a "Log in" section in the
    # navbar for the first time
    # It's telling her to enter her email address, so she does
    browser.get(live_server_url)
    browser.find_element_by_name('email').send_keys(TEST_EMAIL, Keys.ENTER)

    # A message appears telling her an email has been sent
    elem = wait_for(browser.find_element_by_tag_name, 'body')
    assert 'Check your email' in elem.text

    # She checks her email and finds a message
    mail_body = mail_checker.wait_login_mail_content()

    # It has a url link in it
    assert 'Use this link to log in' in mail_body
    url_search = re.search(r'http://.+/.+$', mail_body)
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


class MailChecker:
    def __init__(self):
        if is_staging_server():
            self.inbox = None
            self.reload_inbox()
            self.last_mail_index = self.get_mail_count()

    def reload_inbox(self):
        if self.inbox is not None:
            self.inbox.quit()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        inbox.user(TEST_EMAIL)
        inbox.pass_('rhdrodyd')
        self.inbox = inbox

    def get_mail_count(self):
        return self.inbox.stat()[0]

    def get_mail_content_by_index(self, idx):
        return '\n'.join([l.decode('utf8') for l in self.inbox.retr(idx)[1]])

    def get_new_login_mail(self):
        self.reload_inbox()
        mail_count = self.get_mail_count()
        assert self.last_mail_index < mail_count

        for idx in range(self.last_mail_index + 1, mail_count + 1):
            content = self.get_mail_content_by_index(idx)
            if 'Subject: {}'.format(SUBJECT) in content:
                return content
            else:
                self.last_mail_index = idx
        assert False

    def wait_login_mail_content(self):
        if is_staging_server():
            return wait_for(self.get_new_login_mail, wait_time=60, wait_interval=5)
        else:
            return mail.outbox[0].body
