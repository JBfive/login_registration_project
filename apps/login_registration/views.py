from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *


def index (request):
	return render(request, 'login_registration/index.html')

def process (request):
	errors = User.objects.basic_validator(request.POST)
	if errors['status']== False:
		for key, value in errors['return'].items():
			messages.error(request, value)
		return redirect('/')
	else:
		request.session['user_id']= errors['return']
		print(request.session['user_id'])
		return redirect('/success')
def login (request):
	errors = User.objects.validate_login(request.POST)
	if errors['status']== False:
		for key, value in errors['return'].items():
			messages.error(request, value)
		return redirect('/')
	else:
		request.session['user_id']= errors['return']
		print(request.session['user_id'])
		return redirect('/success')


def success (request):
	user={'user' : User.objects.get(id=request.session['user_id'])}
	return render(request, 'login_registration/success.html', user)

def clear (request):
	request.session.clear()
	return redirect('/') 