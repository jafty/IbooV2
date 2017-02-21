from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.event_list, name='event_list'),
	url(r'^(?P<pk>[0-9]+)/enter$', views.enter_event, name='enter_event'),
	url(r'^(?P<pk>[0-9]+)/$', views.event_detail, name='event_detail'),
	url(r'^new/$', views.event_new, name='event_new'),
	url(r'^(?P<username>\w+)/profile$', views.public_profile, name='public_profile'),
	url(r'^(?P<pk>[0-9]+)/demande$', views.demande, name='demande'),
	url(r'^messagerie/$', views.messagerie, name='messagerie'),
	url(r'^(?P<pk>[0-9]+)/(?P<cand>\w+)/accept$', views.accept, name='accept'),
	url(r'^(?P<pk>[0-9]+)/(?P<cand>\w+)/refuse$', views.accept, name='refuse'),
	url(r'^(?P<pk>[0-9]+)/my_event$', views.my_event, name='my_event'),
	url(r'^(?P<pk>[0-9]+)/edit_my_event$', views.edit_my_event, name='edit_my_event'),
]