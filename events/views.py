from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Message, List
from payment.models import ProviderProfile
from accueil.models import UserProfile
from django.contrib.auth.models import User
from .forms import EventForm, PassForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import urllib.request
import oauth2
import stripe
import json
import rauth
from rauth import OAuth2Service
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

stripe.api_key = "sk_test_umUV6AR8vWmm6HrkHnSFmPga "

# Create your views here.

	
@login_required
def event_list(request):
    now = datetime.today()
    events=Event.objects.filter(date__gte=now).order_by('date')
    return render(request, 'events/event_list.html', {'events':events})
   
@login_required
def event_detail(request, pk):
	event = get_object_or_404(Event, pk=pk)
	user = event.author
	profile = get_object_or_404(UserProfile, user=user)
	return render(request, 'events/event_detail.html', {'event':event, 'profile':profile})

@login_required
def enter_event(request, pk):
	me=request.user
	event=Event.objects.get(pk=pk)
	if List.objects.filter(member=me).exists():
		return render(request, 'payment/charge.html', {'event':event})
	else:
		return render(request, 'events/not_accepted.html',{'events':events})

		





@login_required
def public_profile(request, username):
	# On récupère le profile du mec qui a créé le bail dans une url
	user=get_object_or_404(User, username=username)
	profile=UserProfile.objects.get(user=user)
	events_o=Event.objects.filter(author=user)
	list_p=List.objects.filter(member=user)
	# On affiche les informations relatives à ce mec
	return render(request, 'events/public_profile.html', {'profile': profile, 'events_o':events_o, 'list_p':list_p})

@login_required
def event_new(request):	
    
	me = request.user
	profile = UserProfile.objects.get(user = me)
	if profile.provider==True:
		if ProviderProfile.objects.filter(user = me).exists():
			provider = ProviderProfile.objects.get(user=me)
			stripe_user_id = provider.stripe_user_id
			
			if request.method == "POST":
				form = EventForm(request.POST or None)
				if form.is_valid():
					event = form.save(commit=False)
					event.author = request.user
					event.stripe_user_id = stripe_user_id
					event.save()
					return HttpResponseRedirect(reverse('event_list'))
			else:
				form = EventForm()
			return render(request, 'events/event_new.html', {'form':form})
		else:
			return render(request, 'payment/connect_stripe.html')
	else:
		return render(request, 'events/not_provider.html')

		
def demande(request, pk):
	print(pk)
	print('pd')
	event = get_object_or_404(Event, pk=pk)
	if request.method == "POST":
		form = MessageForm(request.POST or None)
		if form.is_valid():
			demande = form.save(commit=False)
			demande.event = event
			demande.type = 'DM'
			demande.receiver = event.author
			demande.sender = request.user
			demande.save()
			return HttpResponseRedirect(reverse('event_list'))
	else:
		form = MessageForm()
	return render(request, 'events/demande.html', {'form':form})	

def accept(request, pk, cand):
	me=request.user
	candidate=User.objects.get(username=cand)
	event = Event.objects.get(pk=pk)
	Message.objects.create(type='AC', sender=me, receiver=candidate, event=event, msg_content="Vous avez été autorisé à participer à l'évènement")
	Message.objects.filter(event=event, sender=candidate).delete()
	List.objects.create(event=event, member=candidate)
	return render(request, 'events/refuse.html')
	
def refuse(request, pk, cand):
	me=request.user
	candidate=User.objects.get(username=cand)
	event = Event.objects.get(pk=pk)
	Message.objects.create(type='RE', sender=me, receiver=candidate, event=event, msg_content="Vous n'avez pas été autorisé à participer à l'évènement")
	Message.objects.filter(event=event, sender=cand).delete()
	return render(request, 'events/refuse.html')
	

def messagerie(request):
	me=request.user


	messages=Message.objects.filter(receiver=me)
	return render(request, 'events/messagerie.html', {'messages':messages})


def my_event(request, pk):
	me=request.user

	event = Event.objects.get(pk=pk)
	if me==event.author:
		list=List.objects.filter(event=event, paid=True)
		return render(request, 'events/my_event.html', {'list':list, 'event':event})
	else:
		return render(request, 'events/event_list.html')
	
def edit_my_event(request, pk):	
	me=request.user

	event = Event.objects.get(pk=pk)
	if me==event.author:
		if request.method == "POST":
			form = EventForm(request.POST, instance=event)
			if form.is_valid():
				event = form.save(commit=False)
				event.save()
				return HttpResponseRedirect(reverse('profile'))
		else:
			form = EventForm(instance=event)
		return render(request, 'events/edit_my_event.html', {'form':form})
	else:
		return render(request, 'events/event_list.html')	

def delete_my_event(request, pk):	
	me=request.user

	event = Event.objects.get(pk=pk)
	if me==event.author:
		if request.method == "POST":
			Event.objects.filter(author=me).delete()
			return render(request, 'events/event_list.html')
		else:
			form = EventForm(instance=event)
		return render(request, 'events/edit_my_event.html', {'form':form})
	else:
		return render(request, 'events/event_list.html')	
