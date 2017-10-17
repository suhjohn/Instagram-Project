from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login as django_login

import post
from .forms import SignUpForm

# Create your views here.

User = get_user_model()


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # user 가 있으면 값이 있고 없으면 None
        user = authenticate(
            username=username,
            password=password,
        )
        if user is not None:
            django_login(request, user)
            return redirect(post.views.post_list)
        else:
            return HttpResponse('Login credentials invalid')
    else:
        return render(request, 'member/login.html')

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
