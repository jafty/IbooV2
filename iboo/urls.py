from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('accueil.urls')),
	url(r'^events/', include('events.urls')),
	url(r'^payment/', include('payment.urls')),
]