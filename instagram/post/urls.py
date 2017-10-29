from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^delete/(?P<post_pk>\d+)/$', views.post_delete, name='post_delete'),
    url(r'^(?P<post_pk>\d+)/like$', views.post_like_toggle, name='post_like_toggle'),
    url(r'^comment/(?P<post_pk>\d+)/$', views.add_comment, name='add_comment'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.delete_comment, name='delete_comment'),
]
