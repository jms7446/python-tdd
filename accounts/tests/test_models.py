from django.contrib import auth
from accounts.models import Token

EMAIL1 = 'a@b.com'

################################################################################
# User
################################################################################

User = auth.get_user_model()


def test_user_is_valid_with_email_only():
    user = User(email=EMAIL1)
    user.full_clean()   # should not raise


def test_email_is_primary_key():
    user = User(email=EMAIL1)
    assert user.pk == EMAIL1


def test_no_problem_with_auth_login(client):
    user = User.objects.create(email='edith@example.com')
    user.backend = ''
    request = client.request().wsgi_request
    auth.login(request, user)   # should not raise



################################################################################
# Token
################################################################################

def test_links_user_with_auto_generated_uid():
    token1 = Token.objects.create(email=EMAIL1)
    token2 = Token.objects.create(email=EMAIL1)
    assert token1.uid != token2.uid
