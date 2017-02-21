from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^stripe_callback/$', views.stripe_callback, name='stripe_callback'),
	url(r'^(?P<pk>[0-9]+)/charge/$', views.charge, name='charge'),
]