from unittest.mock import patch, call
import pytest

from accounts.views import EMAIL_SENT_SUCCESS_MESSAGE
from accounts.models import Token


@pytest.fixture
def mock_auth():
    with patch('accounts.views.auth') as mock_auth:
        yield mock_auth


################################################################################
# SendLoginEmailView
################################################################################

EDITH_EMAIL = 'edith@example.com'


def send_email_to_edith(client, follow=False):
    return client.post('/accounts/send_login_email',
                       data={'email': EDITH_EMAIL},
                       follow=follow,
                       )


def test_redirects_to_home_page_after_send_email(client, test_case):
    response = send_email_to_edith(client)
    test_case.assertRedirects(response, '/')


@patch('accounts.views.send_mail')
def test_sends_mail_to_address_from_post(send_mail_mock, client):
    send_email_to_edith(client)

    assert send_mail_mock.called == True
    (subject, body, from_email, to_list), kwargs = send_mail_mock.call_args
    assert subject == 'Your login link for Superlists'
    assert 'Use this link to log in' in body
    assert from_email == 'noreply@superlists'
    assert to_list == ['edith@example.com']


def test_adds_success_message(client):
    response = send_email_to_edith(client, follow=True)
    message = list(response.context['messages'])[0]
    assert message.message == EMAIL_SENT_SUCCESS_MESSAGE
    assert message.tags == 'success'


@patch('accounts.views.messages')
def test_adds_success_message_with_mock(messages_mock, client):
    response = send_email_to_edith(client)
    assert messages_mock.success.call_args == call(response.wsgi_request, EMAIL_SENT_SUCCESS_MESSAGE)


################################################################################
# LoginView
################################################################################

def test_redirects_to_home_page_after_login(client, test_case):
    response = client.get('/accounts/login?token=abcd123')
    test_case.assertRedirects(response, '/')


def test_creates_token_associated_with_email(client):
    send_email_to_edith(client)
    token = Token.objects.first()
    assert token.email == EDITH_EMAIL


@patch('accounts.views.send_mail')
def test_sends_link_to_login_using_token_uid(send_mail_mock, client):
    send_email_to_edith(client)
    token = Token.objects.first()
    expected_url = f'http://testserver/accounts/login?token={token.uid}'
    (subject, body, from_email, to_list), kwargs = send_mail_mock.call_args
    assert expected_url in body


def test_calls_authenticate_with_uid_from_get_request(mock_auth, client):
    client.get('/accounts/login?token=abcd123')
    assert mock_auth.authenticate.call_args == call(uid='abcd123')


def test_calls_auth_login_with_user_if_there_is_one(mock_auth, client):
    response = client.get('/accounts/login?token=abcd123')
    assert mock_auth.login.call_args == call(response.wsgi_request, mock_auth.authenticate.return_value)


def test_does_not_login_if_user_is_not_authenticated(mock_auth, client):
    mock_auth.authenticate.return_value = None
    client.get('/accounts/login?token=abcd123')
    assert mock_auth.login.called == False
