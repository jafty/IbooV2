from django.contrib import admin
from .models import List, Event, Message

admin.site.register(Event)
admin.site.register(List)
admin.site.register(Message)