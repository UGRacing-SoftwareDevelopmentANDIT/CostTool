from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from tool.models import UserAccount, Car
from django.db.models import Sum, F
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from tool.forms import UserForm, UserAccountForm

########################################## Base ###############################################
def home(request):
	#for top 3 of week - returns list of length 3 in order
	context_dict = {}

	car_list = Car.objects.order_by('carYear')[:5]

	context_dict['test'] = 'test'
	context_dict['cars'] =  car_list
	response = render(request, 'tool/home.html', context=context_dict)
	return response


def about(request):
	#information page
	context_dict = {}
	return render(request, 'tool/about.html', context=context_dict)


def car_display(request, car_slug):
	context_dict ={}
	try:
		car = Car.objects.get(carSlug = car_slug)
		context_dict['Car'] = car
		print( car.carName )
	except Car.DoesNotExist:
		context_dict['Car'] = None			
			
	return render(request, 'tool/car_display.html', context = context_dict)