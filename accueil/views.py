from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import UserProfile 
from events.models import Event
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required


from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# Create your views here.
def index(request):
    return render(request, 'accueil/index.html')

def mode_emploi(request):
    return render(request, 'accueil/mode_emploi.html')

def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			username=form.cleaned_data['username'],
			password=form.cleaned_data['password1'],
			email=form.cleaned_data['email']
			)
			events = Event.objects.all()
			return HttpResponseRedirect(reverse('confirm'))
	else:
		form = RegistrationForm()
	return render(request, 'accueil/register.html', {'form':form})

def confirm(request):
	return render(request, 'accueil/confirm.html')
	
def profile(request):
	user_profile = UserProfile.objects.get(user=request.user)
	events_o = Event.objects.filter(author=request.user)
	
	return render(request, 'accueil/profile.html', {'user_profile':user_profile, 'events_o':events_o})
	

def edit_profile(request):	
	me = request.user

# at least one object satisfying query exists

	profile = UserProfile.objects.get(user=me)
	if request.method == "POST":
		form = UserProfileForm(request.POST, instance=profile)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.save()
			return HttpResponseRedirect(reverse('profile'))
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'accueil/edit_profile.html', {'form':form})

 

	

