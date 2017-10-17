"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from member.views import (
    signup,
    login)
from post.views import (
    post_list,

    post_create, add_comment, post_detail)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Post application
    url(r'^post/$', post_list, name='post_list'),
    url(r'^post/(?P<post_pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^post/create/$', post_create, name='post_create'),
    url(r'comment/(?P<post_pk>\d+)/$', add_comment, name='add_comment'),

    # Member
    url(r'^member/signup', signup, name='signup'),
    url(r'^member/login/$', login, name='login'),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
