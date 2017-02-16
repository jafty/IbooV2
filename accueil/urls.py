from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^confirm/$', views.confirm, name='confirm'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
	
]