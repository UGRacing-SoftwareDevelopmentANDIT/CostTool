from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from tool.models import *
from django.db.models import Sum, F
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from tool.forms import *

########################################## Base ###############################################


def home(request):
    context_dict = {}

    car_list = Car.objects.order_by('carYear')[:5]

    context_dict['test'] = 'test'
    context_dict['cars'] = car_list
    response = render(request, 'tool/home.html', context=context_dict)
    return response


def about(request):
    # information page
    context_dict = {}
    return render(request, 'tool/about.html', context=context_dict)

########################################## Displays ###############################################


def car_display(request, car_slug):
    context_dict = {}
    try:
        car = Car.objects.get(carSlug=car_slug)
        systems = System.objects.filter(carID=car)

        context_dict['car'] = car
        context_dict['systems'] = systems

    except Car.DoesNotExist:
        context_dict['car'] = None

    return render(request, 'tool/car_display.html', context=context_dict)


def system_display(request, system_slug, car_slug):
    context_dict = {}
    try:
        system = System.objects.get(systemSlug=system_slug)
        car = Car.objects.get(carSlug=car_slug)
        assemblys = Assembly.objects.filter(systemID=system)

        context_dict['system'] = system
        context_dict['car'] = car
        context_dict['assemblys'] = assemblys

    except System.DoesNotExist:
        context_dict['System'] = None

    return render(request, 'tool/system_display.html', context=context_dict)


def assembly_display(request, assembly_slug, system_slug, car_slug):
    context_dict = {}
    try:
        assembly = Assembly.objects.get(assemblySlug=assembly_slug)
        system = System.objects.get(systemSlug=system_slug)
        car = Car.objects.get(carSlug=car_slug)

        parts = Part.objects.filter(assemblyID=assembly)

        context_dict['system'] = system
        context_dict['car'] = car
        context_dict['assembly'] = assembly
        context_dict['parts'] = parts

    except System.DoesNotExist:
        context_dict['System'] = None

    return render(request, 'tool/assembly_display.html', context=context_dict)


def part_display(request, part_slug, assembly_slug, system_slug, car_slug):
    context_dict = {}
    try:
        part = Part.objects.get(partSlug=part_slug)
        assembly = Assembly.objects.get(assemblySlug=assembly_slug)
        system = System.objects.get(systemSlug=system_slug)
        car = Car.objects.get(carSlug=car_slug)

        pmfts = PMFT.objects.filter(partID=part)

        context_dict['system'] = system
        context_dict['car'] = car
        context_dict['assembly'] = assembly
        context_dict['part'] = part

        context_dict['pmfts'] = pmfts

    except System.DoesNotExist:
        context_dict['System'] = None

    return render(request, 'tool/part_display.html', context=context_dict)


def pmft_display(request, pmft_slug, part_slug, assembly_slug, system_slug, car_slug):
    context_dict = {}
    try:
        pmft = PMFT.objects.get(pmftSlug=pmft_slug)
        part = Part.objects.get(partSlug=part_slug)
        assembly = Assembly.objects.get(assemblySlug=assembly_slug)
        system = System.objects.get(systemSlug=system_slug)
        car = Car.objects.get(carSlug=car_slug)

        pmfts = PMFT.objects.filter(partID=part)

        context_dict['pmft'] = pmft
        context_dict['part'] = part
        context_dict['system'] = system
        context_dict['car'] = car
        context_dict['assembly'] = assembly

    except System.DoesNotExist:
        context_dict['System'] = None

    return render(request, 'tool/pmft_display.html', context=context_dict)

    ########################################## Forms ###############################################


def add_car(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    form = AddCarForm()
    # user verification stuff for later (not an outer if(verifed)) else print (form.errors) and  return HttpResponse("This page is exclusively for cost heads")
    '''
        # get user ID
    userID = request.user.get_username()
        # get user object
    users = User.objects.filter(username=userID)
        # get if user is verified
    verified = UserAccount.objects.filter(user__in=users, verified=True)
        '''

    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            newCar = form.save(commit=False)
            # save details
            newCar.save()
            return redirect(reverse('tool:home'))
        else:
            print(form.errors)

    return render(request, 'tool/add_car.html', {'form': form})
  
  
def add_system(request, car_slug):
    context_dict = {}
    form = AddSystemForm()
    car = Car.objects.get(carSlug=car_slug)
    context_dict['car'] = car
    if request.method == 'POST':
        form = AddSystemForm(request.POST)
        if form.is_valid():
            newSystem = form.save(commit=False)
            newSystem.carID = Car.objects.get(carSlug=car_slug)
            newSystem.save()
            return redirect(reverse('tool:home'))
        else:
            print(form.errors)
    return render(request, 'tool/add_system.html', {'form': form, 'context': context_dict})


def add_assembly(request, car_slug, system_slug):
    context_dict = {}
    try:
        system = System.objects.get(systemSlug=system_slug)

        context_dict['system'] = system
        context_dict['car_slug'] = car_slug
        context_dict['system_slug'] = system_slug

    except System.DoesNotExist:
        context_dict['system'] = None

    form = AddAssemblyForm()
    if request.method == 'POST':
        form = AddAssemblyForm(request.POST)
        if form.is_valid():
            newAssembly = form.save(commit=False)
            newAssembly.systemID = System.objects.get(systemSlug=system_slug)
            newAssembly.save()
            return redirect(reverse('tool:system_display', args=[car_slug, system_slug]))
        else:
            print(form.errors)
    context_dict["form"] = form

    return render(request, 'tool/add_assembly.html', context_dict)
  
  
def add_part(request, car_slug, system_slug, assembly_slug):
    context_dict = {}
    
    assembly = Assembly.objects.get(assemblySlug= assembly_slug)
    context_dict['assembly'] = assembly

    context_dict['carSlug'] = car_slug
    context_dict['systemSlug'] = system_slug


    form = AddPartForm()
    if request.method == 'POST':
        form = AddPartForm(request.POST)
        if form.is_valid():
            newPart = form.save(commit=False)

            newPart = form.save(commit=False)
            newPart.assemblyID = Assembly.objects.get(assemblySlug=assembly_slug)

            # save details
            newPart.save()
            return redirect(reverse('tool:home'))
        else:
            print(form.errors)

    return render(request, 'tool/add_part.html', {'form': form, 'context': context_dict})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        account_form = UserAccountForm(request.POST)
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            registered = True
        else:
            print(user_form.errors, account_form.errors)
    else:
        user_form = UserForm()
        account_form = UserAccountForm()
    
    return render(request,
                    'tool/register.html',
                    context={'user_form': user_form,
                                'account_form': account_form,
                                'registered': registered})

