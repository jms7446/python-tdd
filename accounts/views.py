import sys

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from django.urls import reverse

from accounts.models import Token

EMAIL_SENT_SUCCESS_MESSAGE = "Check your email, we've sent you a link you can use to login."


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists',
        [email],
    )
    messages.success(request, EMAIL_SENT_SUCCESS_MESSAGE)

    return redirect('/')


def login(request):
    uid = request.GET.get('token')
    user = auth.authenticate(uid=uid)
    if user:
        auth.login(request, user)
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')
