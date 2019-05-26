from .conftest import *


def test_logged_in_users_lists_are_saved_as_my_lists(browser, live_server_url):
    email = 'edith@example.com'
    browser.get(live_server_url)
    wait_to_be_logged_out(browser, email)

    # Edith is logged-in user
    create_pre_authenticated_session(email, browser, live_server_url)
    browser.get(live_server_url)
    wait_to_be_logged_in(browser, email)
