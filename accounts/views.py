import uuid
import sys

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

from accounts.models import Token


def send_mail(title, content, fr):
    print('=' * 80)
    print('= send mail')
    print(title)
    print(content)
    print(fr)
    print('=' * 80)


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print(f'saving uid {uid}, for email {email}', file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in: \n\n{url}',
        'noreply@superlists',
    )
    return render(request, 'login_email_sent.html')


def login(request):
    uid = request.GET.get('uid')

    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')
