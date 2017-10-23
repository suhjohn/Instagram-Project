from urllib.parse import urlparse

from django.http import request
from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    def decorator(*args, **kwargs):
        if not bool(args[0].user.is_authenticated):
            referer = urlparse(request.META['HTTP_REFERER']).path
            url = f'{reverse("member:login")}?next={referer}'
            return redirect(url)
        return view_func(*args, **kwargs)
    return decorator