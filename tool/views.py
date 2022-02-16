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
from tool.consts import USER_RANKS

########################################## Base ###############################################

# TODO: Stop logging out, breaking the web app
def home(request):
    context_dict = {}

    car_list = Car.objects.filter(archived = False).order_by('carYear')
    archived_car_list = Car.objects.filter(archived = True).order_by('carYear')
    user_account, user_rank = get_user_details(request)

    context_dict['test'] = 'test'
    context_dict['cars'] = car_list
    context_dict['archived_cars'] = archived_car_list
    context_dict['user_rank'] = user_rank
    context_dict["display_add_car"] = False
    context_dict["display_edit_car"] = False

    if user_account.rank >= 4:
        context_dict["display_add_car"] = True
        context_dict["display_edit_car"] = True

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
        user_account, user_rank = get_user_details(request)
        car = Car.objects.get(carSlug=car_slug)
        systems = System.objects.filter(carID=car)

        context_dict['car'] = car
        context_dict['systems'] = systems
        context_dict['archived'] = car.archived
        context_dict['user_rank'] = user_rank

        #accesss_bool : systemID -> (access the system , eddit the system)
        context_dict['access_bool'] = {}
        access_bool = {}

        #display_add_system is defined here as it only shows once on page
        #display_edit_subteam is defined here because its value only depends on user and is the same for all systems
        if car.archived:
            context_dict['display_add_system'] = False
            context_dict['display_edit_subteam'] = False
        elif user_account.rank >= 4:
            context_dict['display_add_system'] = True
            context_dict['display_edit_subteam'] = True
        else:
            context_dict['display_add_system'] = False
            context_dict['display_edit_subteam'] = False

        for system in systems:
            #if a car is archived no edditing regardless of user/system
            if car.archived:
                    access_bool[system.systemID] = (False, False)
            #is a user is CH they have full priviledges for all systems        
            elif user_account.rank >= 4:
                    access_bool[system.systemID] = (True, True)
            else:
                subteams = Subteam.objects.filter(systems=system)        
                assignedTH = False
                assignedEng = False 
                for subteam in subteams:
                    #if a user is linked to a subteam that is assigned to the system
                    if TeamLinking.objects.filter(user=user_account, subteam=subteam).exists():
                        #if the above linking is that of a team head
                        if TeamLinking.objects.filter(user=user_account, subteam=subteam, teamHead=True).exists():
                            assignedTH = True
                        else:
                            assignedEng = True
                if assignedEng:
                    #if assigned and not a TH     
                    access_bool[system.systemID] = (True, False)
                elif assignedTH:
                    #if assigned and a TH
                    access_bool[system.systemID] = (True, True)  
                else:
                    #if they are never in a assigned subteam
                    access_bool[system.systemID] = (False, False)                                

        context_dict['access_bool'] = access_bool

    except Car.DoesNotExist:
        context_dict['car'] = None

    return render(request, 'tool/car_display.html', context=context_dict)

@login_required
def system_display(request, system_slug, car_slug):
    context_dict = {}
    try:
        user_account, user_rank = get_user_details(request)
        system = System.objects.get(systemSlug=system_slug)
        car = Car.objects.get(carSlug=car_slug)
        assemblys = Assembly.objects.filter(systemID=system)


        sysAssignedTH = False
        sysAssigned = False

        #access_bool: assemblyID -> = can edit assembly
        access_bool = {}
        output = {}
        subteams = Subteam.objects.filter(systems=system)
        
        #makes sure a user can only see the page if in assigned subteam
        for subteam in subteams:
            if TeamLinking.objects.filter(user=user_account, subteam=subteam).exists():
                sysAssigned= True
            if user_account.rank >= 4 or TeamLinking.objects.filter(user=user_account, subteam=subteam, teamHead=True).exists():
                sysAssignedTH = True
        if not sysAssigned:
            return redirect('tool:car_display', car_slug=car_slug)

        #display_eddit_assignees is the same regardless of assembly
        #display_add_assembly is the same regardless of assembly
        if car.archived:
            context_dict['display_add_assembly'] = False
            context_dict['display_edit_assignees'] = False
        elif user_account.rank > 4:
            context_dict['display_add_assembly'] = True
            context_dict['display_edit_assignees'] = True
        elif sysAssignedTH:
            context_dict['display_add_assembly'] = True
            context_dict['display_edit_assignees'] = True
        else:
            context_dict['display_add_assembly'] = False
            context_dict['display_edit_assignees'] = False   

        for assembly in assemblys:
            if car.archived:
                access_bool[assembly.assemblyID] = False
            elif user_account.rank > 4:
                access_bool[assembly.assemblyID] = True
            elif sysAssignedTH:
                access_bool[assembly.assemblyID] = True
            else :
                if user_account == assembly.user:
                    #eingineer has been assigned
                    access_bool[assembly.assemblyID] = True
                else:
                    #eingineer has not been assigned
                    access_bool[assembly.assemblyID] = False
            parts = Part.objects.filter(assemblyID=assembly.assemblyID)
            output[assembly] = {}
            for part in parts:
                pmfts = PMFT.objects.filter(partID=part.partID)
                output[assembly][part] = list(pmfts)


        context_dict['system'] = system
        context_dict['car'] = car
        context_dict['assemblys'] = assemblys
        context_dict['output'] = output
        context_dict['user_rank'] = user_rank

    except System.DoesNotExist:
        context_dict['System'] = None

    return render(request, 'tool/system_display.html', context=context_dict)


    ########################################## Car Forms ###############################################


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


def add_pmft(request, car_slug, system_slug, assembly_slug, part_slug):
    context_dict = {}
    
    part = Part.objects.get(partSlug=part_slug)
    context_dict['assemblySlug'] = assembly_slug
    context_dict['carSlug'] = car_slug
    context_dict['systemSlug'] = system_slug
    context_dict['part'] = part


    form = AddPMFTForm()
    if request.method == 'POST':
        form = AddPMFTForm(request.POST)
        if form.is_valid():
            newPMFT = form.save(commit=False)

            newPMFT = form.save(commit=False)
            newPMFT.partID = Part.objects.get(partSlug=part_slug)

            # save details
            newPMFT.save()
            return redirect(reverse('tool:home'))
        else:
            print(form.errors)

    return render(request, 'tool/add_pmft.html', {'form': form, 'context': context_dict})


########################################## User Forms ###############################################

def edit_subteam(request, car_slug, system_slug):
    context_dict = {}

    system = System.objects.get(systemSlug=system_slug)
    subteams = Subteam.objects.filter(systems = system)

    context_dict['carSlug'] = car_slug
    context_dict['systemSlug'] = system_slug
    context_dict['subteams'] = subteams

    form = EditSubteam()
    if request.method == 'POST':
        form = EditSubteam(request.POST)
        if form.is_valid():
            subteam = Subteam.objects.get(teamName = form['subteamQ'].value())
            subteam.systems.add(system)
            return redirect(reverse('tool:edit_subteam', args=[car_slug, system_slug]))
        else:
            print(form.errors)

    return render(request, 'tool/edit_subteam.html', {'form': form, 'context': context_dict})


def delete_subteam(request, car_slug, system_slug, subteam_slug):
     system = System.objects.get(systemSlug=system_slug)
     subteam = Subteam.objects.get(subteamSlug = subteam_slug)

     subteam.systems.remove(system)
     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def edit_assign_eng(request, car_slug, system_slug, assembly_slug):
    context_dict = {}


    assembly = Assembly.objects.get(assemblySlug = assembly_slug)

    currentEng = assembly.user

    context_dict['carSlug'] = car_slug
    context_dict['systemSlug'] = system_slug
    context_dict['assemblySlug'] = assembly_slug
    context_dict['currentEng'] = currentEng

    form = EditAssignEng()
    if request.method == 'POST':
        form = EditAssignEng(request.POST)
        if form.is_valid():
            user = UserAccount.objects.get(pk = form['engineer'].value())
            assembly.user = user
            assembly.save()
            return redirect(reverse('tool:system_display', args=[car_slug, system_slug]))
        else:
            print(form.errors)

    return render(request, 'tool/edit_assign_eng.html', {'form': form, 'context': context_dict})


########################################## User Logins ###############################################

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


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('tool:home'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details.")
    else:
        return render(request, 'tool/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('tool:home'))




########################################## Helper Functions ###############################################


def get_user_details(request):
    user_account = UserAccount.objects.get(pk=request.user)
    user_rank = USER_RANKS[user_account.rank]

    return user_account, user_rank
