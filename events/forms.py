import re
from django import forms
from django.contrib.auth.models import User
from .models import Event, Message
from django.utils.translation import ugettext_lazy as _


		
class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'date', 'description', 'drink', 'food', 'address', 'price',)
		
        labels = {
            'title': _('Nom de votre évènement'),
			'date': _('Date (YYYY-MM-DD)'),
			'price': _('Prix (en centimes)'),
			'drink': _('Boissons ?'),
			'food': _('Nourriture ?'),
            'description': _('Description'),
            'address': _('Adresse'),
        }

class PassForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput())

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('msg_content',)
		
        labels = {
            'msg_content': _("Dites deux trois mots à l'organisateur pour avoir plus de chances d'être accepté !"),
        }