from typing import NamedTuple

import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout as django_logout, login as django_login
from django.urls import reverse

import post
from config import settings
from .forms import SignUpForm, LoginForm

# Create your views here.

User = get_user_model()


def login(request):
    """
    로그인 기능
    :param request:
    :return:
    """
    next_path = request.GET.get('next')
    login_form = LoginForm(request.POST, )

    if login_form.is_valid():
        login_form.login(request)
        if next_path:
            return redirect(next_path)
        return redirect('post:post_list')

    context = {
        'login_form': login_form,
        'facebook_app_scope': ','.join(settings.FACEBOOK_APP_SCOPE),
        'facebook_app_id': settings.FACEBOOK_APP_ID,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    """
    로그아웃 기능
    :param request:
    :return:
    """
    django_logout(request)
    return redirect('member:login')


def signup(request):
    """
    회원가입 기능
    :param request:
    :return:
    """
    signup_form = SignUpForm(request.POST, request.FILES, )
    if signup_form.is_valid():
        new_user = signup_form.save(commit=False)
        new_user.save()
        django_login(request, new_user)
        return redirect('post:post_list')
    context = {
        'signup_form': signup_form
    }

    return render(request, 'member/sign_up.html', context)


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: list
        type: str
        user_id: str

    url_access_token = "https://graph.facebook.com/v2.10/oauth/access_token"
    app_id = settings.FACEBOOK_APP_ID
    app_secret = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret}'
    code = request.GET.get('code')

    def get_access_token_info(code):
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook_login')
        )
        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret,
            'code':code,
        }
        response_1 = requests.get(url_access_token, params_access_token)
        return AccessTokenInfo(**response_1.json())

    def get_debug_token_info(token):
        url_debug_token = "https://graph.facebook.com/debug_token"

        params_data = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_data)
        return DebugTokenInfo(**response.json()['data'])

    access_token = get_access_token_info(code).access_token
    debug_token_info = get_debug_token_info(access_token)

    user_info_fields = [
        'id',
        'name',
        'picture',
        'email',
    ]
    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token':access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()
    return HttpResponse(result.items())






