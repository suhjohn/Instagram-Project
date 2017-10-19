from django.conf.urls import url

from member import views

urlpatterns = [
    url(r'^signup', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
