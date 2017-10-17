from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout as django_logout

import post
from .forms import SignUpForm, LoginForm

# Create your views here.

User = get_user_model()


def login(request):
    login_form = LoginForm(request.POST,)
    if login_form.is_valid():
        login_form.login(request)
        return redirect(post.views.post_list)
    context = {
        'login_form':login_form,
    }
    return render(request, 'member/login.html', context)

def signup(request):
    signup_form = SignUpForm(request.POST, )
    if signup_form.is_valid():
        username = signup_form.cleaned_data['username']
        password = signup_form.cleaned_data['password']
        new_user = User.objects.create_user(username=username, password=password)
        return (HttpResponse(f'<p>{new_user.username}</p>'))
    context = {
        'signup_form': signup_form
    }

    return render(request, 'member/sign_up.html', context)
