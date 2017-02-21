from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	profile_pic_url = models.CharField(max_length=200, blank=True)
	description = models.TextField(blank=True)
	numero = models.CharField(max_length=10, blank=True)
	age = models.CharField(max_length=50, blank=True)
	profession = models.CharField(max_length=50, blank=True)
	provider= models.BooleanField(default=False)
	
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    print("before_if")
    if created:
        print("after if")
        UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()
	