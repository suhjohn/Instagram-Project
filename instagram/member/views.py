from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout as django_logout, login as django_login

import post
from .forms import SignUpForm, LoginForm

# Create your views here.

User = get_user_model()


def login(request):
    """
    로그인 기능
    :param request:
    :return:
    """
    login_form = LoginForm(request.POST,)
    if login_form.is_valid():
        login_form.login(request)
        return redirect('post:post_list')
    context = {
        'login_form':login_form,
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
    signup_form = SignUpForm(request.POST, request.FILES,)
    if signup_form.is_valid():
        new_user = signup_form.save(commit=False)
        new_user.save()
        django_login(request, new_user)
        return redirect('post:post_list')
    context = {
        'signup_form': signup_form
    }

    return render(request, 'member/sign_up.html', context)
