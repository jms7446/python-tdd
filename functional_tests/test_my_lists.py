from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from .conftest import *


def _create_pre_authenticated_session(email, browser, server_url):
    if get_staging_server():
        session_key = create_session_on_server(get_staging_server(), email)
    else:
        session_key = create_pre_authenticated_session(email)

    ## to set a cookie we need to first visit the domain.
    ## 404 pages load the quickest!
    browser.get(server_url + "/404_no_such_url/")
    browser.add_cookie(dict(
        name=settings.SESSION_COOKIE_NAME,
        value=session_key,
        path='/',
    ))


def test_logged_in_users_lists_are_saved_as_my_lists(browser, live_server_url):
    email = 'edith@example.com'
    browser.get(live_server_url)
    wait_to_be_logged_out(browser, email)

    # Edith is logged-in user
    _create_pre_authenticated_session(email, browser, live_server_url)
    browser.get(live_server_url)
    wait_to_be_logged_in(browser, email)
