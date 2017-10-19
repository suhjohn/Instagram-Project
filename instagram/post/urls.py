from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^comment/(?P<post_pk>\d+)/$', views.add_comment, name='add_comment'),
]
