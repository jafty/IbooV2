from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your models here.
class ProviderProfile(models.Model):
	user = models.ForeignKey(User)
	access_token = models.CharField(max_length=50)
	stripe_user_id = models.CharField(max_length=50)

