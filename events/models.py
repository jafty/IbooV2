from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime, date

class Event(models.Model):
	author = models.ForeignKey('auth.User')
	date = models.DateField(default=datetime.now)
	price = models.IntegerField(default=0)
	title = models.CharField(max_length=50)
	description = models.TextField()
	drink = models.BooleanField(default=False)
	food = models.BooleanField(default=False)
	stripe_user_id = models.CharField(max_length=140, default='SOME STRING')
	address = models.CharField(max_length=50)
		
	@property
	def is_past_due(self):
		return date.today() > self.date
		
	def __str__(self):
		return self.title

class Message(models.Model):
    TYPE_MESSAGE = (
        ('DM', 'Demande'),
        ('RE', 'Refus'),
        ('AC', 'Accept'),
    )
    type = models.CharField(
        max_length=2,
        choices=TYPE_MESSAGE,
        default='DM',
    )
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    event = models.ForeignKey(Event, related_name="msg_event")
    msg_content = models.TextField()
    
    def __str__(self):
        return self.sender.username
		
class List(models.Model):
	member = models.ForeignKey(User, related_name="member")
	event = models.ForeignKey(Event, related_name="list_event")
	paid = models.BooleanField(default=False)
	
	def __str__(self):
		return self.member.username


	
