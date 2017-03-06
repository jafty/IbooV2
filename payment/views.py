from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from events.models import Event, List
from accueil.models import UserProfile 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ProviderProfile
import urllib.request
import oauth2
import stripe
import json
import rauth
from rauth import OAuth2Service
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

stripe.api_key = "sk_test_umUV6AR8vWmm6HrkHnSFmPga "

# Create your views here.


@login_required
def charge(request, pk):
	event = get_object_or_404(Event, pk=pk)
	stripe.api_key =  "sk_test_umUV6AR8vWmm6HrkHnSFmPga" 
	token = request.POST['stripeToken']
	event_price = event.price
	percentage = round(event_price*20/100)
	

	# Charge the user's card:
	charge = stripe.Charge.create(
		amount=event.price,
		currency="eur",
		description="Example charge",
		source=token,
		destination=event.stripe_user_id,
		application_fee=percentage,
	)
	list=List.objects.get(member=request.user, event=event)
	list.paid=True
	list.save()


	return render(request, 'payment/confirm.html', {'event':event})
	

@login_required
def connect_stripe(request):

	return render(request, 'payment/connect_stripe.html')


@login_required	
def stripe_callback(request):
    stripe_connect_service = OAuth2Service(
        name = 'stripe',
        client_id = 'ca_A1MFPeV3GsQiotVP31CRHCv31jRmwkPZ',
        client_secret = 'sk_test_umUV6AR8vWmm6HrkHnSFmPga',
        authorize_url = 'https://connect.stripe.com/oauth/authorize',
        access_token_url = 'https://connect.stripe.com/oauth/token',
        base_url = 'https://api.stripe.com/',
    )
	
    code = request.GET['code']
	
    data = {
        'grant_type': 'authorization_code',
        'code': code,
    }
    resp = stripe_connect_service.get_raw_access_token(method='POST', data=data)
    print(resp)
    
    stripe_payload = json.loads(resp.text)
    print(stripe_payload)
    stripe_user_id = stripe_payload["stripe_user_id"]
    print(stripe_payload)
    access_token = stripe_payload["access_token"]
	
    #creer une classe profile 
    me = request.user
    ProviderProfile.objects.create(user=me, stripe_user_id=stripe_user_id, access_token=access_token)
    new_user=ProviderProfile.objects.get(user=me)
    return render(request, 'payment/stripe_callback.html', {'new_user':new_user})
	

			
