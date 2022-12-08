from hashlib import new
import sys
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from tool.models import *
from django.db.models import Sum, F
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from django.template.defaulttags import register

from tool.forms import *
from tool.consts import USER_RANKS

##test push


########################################## Base ###############################################

@login_required
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

@login_required
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
        systemSubteams = {}

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
            subteams = Subteam.objects.filter(systems=system)
            systemSubteams[system.systemID] = subteams        
            #if a car is archived no edditing regardless of user/system
            if car.archived:
                    access_bool[system.systemID] = (False, False)
            #is a user is CH they have full priviledges for all systems        
            elif user_account.rank >= 4:
                    access_bool[system.systemID] = (True, True)
            else:
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
        context_dict['systemSubteams'] = systemSubteams

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

        costHead = False
        sysAssignedTH = False
        sysAssigned = False

        #access_bool: assemblyID -> = can edit assembly
        access_bool = {}
        output = {}
        subteams = Subteam.objects.filter(systems=system)

        #makes sure a user can only see the page if in assigned subteam
        if user_account.rank >= 4:
            costHead = True
        for subteam in subteams:
            if TeamLinking.objects.filter(user=user_account, subteam=subteam).exists():
                sysAssigned= True  
            if  TeamLinking.objects.filter(user=user_account, subteam=subteam, teamHead=True).exists():
                sysAssignedTH = True
        if not (sysAssigned or sysAssignedTH or costHead):
           return redirect('tool:car_display', car_slug=car_slug)

        #display_eddit_assignees is the same regardless of assembly
        #display_add_assembly is the same regardless of assembly

        if car.archived:
            context_dict['display_add_assembly'] = False
            context_dict['display_edit_assignees'] = False
        elif user_account.rank >= 4:
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
            elif user_account.rank >= 4:
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
        context_dict['access_bool'] = access_bool 


    except System.DoesNotExist:
        context_dict['System'] = None

    return render(request, 'tool/system_display.html', context=context_dict)


@register.filter
def get_edit_assembly(dictionary, key):
    return dictionary.get(key)

    ########################################## Car Forms ###############################################


@login_required
def add_car(request, car_slug=None):
    context_dict = {}
    car = None
    context_dict['car'] = car
    
    '''
    # user verification stuff for later (not an outer if(verifed)) else print (form.errors) and  return HttpResponse("This page is exclusively for cost heads")
    # get user ID
    userID = request.user.get_username()
    # get user object
    users = User.objects.filter(username=userID)
    # get if user is verified
    verified = UserAccount.objects.filter(user__in=users, verified=True)
    '''

    if car_slug:
        car = get_object_or_404(Car, carSlug=car_slug)
        form = CarForm(request.POST, instance=car)
    else:
        form = CarForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        newCar = form.save(commit=False)
        if not car_slug:
            newCar.carID = newCar.carName + str(newCar.carYear)
        newCar.save()
        return redirect(reverse('tool:home'))

    context_dict['form'] = form
    if car_slug:
        context_dict['edit'] = True
        context_dict['car'] = car
    else:
        context_dict['edit'] = False

    return render(request, 'tool/add_car.html', context_dict)
  

@login_required
def add_system(request, car_slug, system_slug=None):
    context_dict = {}
    context_dict['car'] = Car.objects.get(carSlug=car_slug)
    system = None
    context_dict['system'] = system

    if system_slug:
        system = get_object_or_404(System, systemSlug=system_slug)
        form = SystemForm(request.POST, instance=system)
    else:
        form = SystemForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        newSystem = form.save(commit=False)
        if not system_slug:
            newSystem.carID = Car.objects.get(carSlug=car_slug)
        systemName = form.cleaned_data.get('systemName')    
        newSystem.systemName = systemName[0]    
        newSystem.save()
        newSystem.save()
        return redirect(reverse('tool:car_display', args=[car_slug]))

    context_dict['form'] = form
    if system_slug:
        context_dict['edit'] = True
        context_dict['system'] = system
    else:
        context_dict['edit'] = False

    return render(request, 'tool/add_system.html', context_dict)


@login_required
def add_assembly(request, car_slug, system_slug, assembly_slug=None):
    context_dict = {}
    context_dict['car'] = Car.objects.get(carSlug=car_slug)
    context_dict['system'] = System.objects.get(systemSlug=system_slug)
    assembly = None
    context_dict['assembly'] = assembly

    if assembly_slug:
        assembly = get_object_or_404(Assembly, assemblySlug=assembly_slug)
        form = AssemblyForm(request.POST, instance=assembly)
    else:
        form = AssemblyForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        newAssembly = form.save(commit=False)
        if not assembly_slug:
            newAssembly.systemID = System.objects.get(systemSlug=system_slug)
        newAssembly.save()
        newAssembly.save()
        return redirect(reverse('tool:system_display', args=[car_slug, system_slug]))
    context_dict['form'] = form
    if assembly_slug:
        context_dict['edit'] = True
        context_dict['assembly'] = assembly
    else:
        context_dict['edit'] = False
        
    return render(request, 'tool/add_assembly.html', context_dict)
  

@login_required
def add_part(request, car_slug, system_slug, assembly_slug, part_slug=None):
    context_dict = {}
    car = Car.objects.get(carSlug=car_slug)
    system = System.objects.get(systemSlug=system_slug)
    assembly = Assembly.objects.get(assemblySlug=assembly_slug)

    context_dict['car'] = car
    context_dict['system'] = system
    context_dict['assembly'] = assembly
    context_dict['costed'] = system.costed

    if part_slug:
        part = get_object_or_404(Part, partSlug=part_slug)
        form = PartForm(request.POST, instance=part)
    else:
        form = PartForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        newPart = form.save(commit=False)
        if not part_slug:
            newPart.assemblyID = Assembly.objects.get(assemblySlug=assembly_slug)
        newPart.save()
        newPart.save()
        return redirect(reverse('tool:system_display', args=[car_slug, system_slug]))

    context_dict['form'] = form
    if part_slug:
        context_dict['edit'] = True
        context_dict['part'] = part
    else:
        context_dict['edit'] = False

    return render(request, 'tool/add_part.html', context_dict)


@login_required
def add_pmft(request, car_slug, system_slug, assembly_slug, part_slug, pmft_slug=None):
    context_dict = {}
    car = Car.objects.get(carSlug=car_slug)
    system = System.objects.get(systemSlug=system_slug)
    assembly = Assembly.objects.get(assemblySlug=assembly_slug)
    part = Part.objects.get(partSlug=part_slug)

    context_dict['car'] = car
    context_dict['system'] = system
    context_dict['assembly'] = assembly
    context_dict['part'] = part
    context_dict['costed'] = system.costed


    if pmft_slug:
        pmft = get_object_or_404(PMFT, pmftSlug=pmft_slug)
        form = PMFTForm(request.POST, instance=pmft)
    else:
        form = PMFTForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        newPMFT = form.save(commit=False)
        if not pmft_slug:
            newPMFT.partID = Part.objects.get(partSlug=part_slug)
        pmftType = form.cleaned_data.get('pmftType')    

        newPMFT.pmftType = pmftType[0]

        if system.costed:
            pmftCostComment = form.cleaned_data.get('pmftCostComment') 
            newPMFT.pmftCostComment = pmftCostComment[0]    
        else:
            newPMFT.pmftCostComment = None
        newPMFT.save()
        newPMFT.save()
        return redirect(reverse('tool:system_display', args=[car_slug, system_slug]))

    context_dict['form'] = form
    if pmft_slug:
        context_dict['edit'] = True
        context_dict['pmft'] = pmft
    else:
        context_dict['edit'] = False

    return render(request, 'tool/add_pmft.html', context_dict)


########################################## User Forms ###############################################

@login_required
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


@login_required
def delete_subteam(request, car_slug, system_slug, subteam_slug):
     system = System.objects.get(systemSlug=system_slug)
     subteam = Subteam.objects.get(subteamSlug = subteam_slug)

     subteam.systems.remove(system)
     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
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
    context_dict = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('tool:home'))
            else:
                return render(request, 'tool/login.html')
        else:
            return render(request, 'tool/login.html')
    else:
        return render(request, 'tool/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('tool:home'))

  
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('tool:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'tool/change_password.html', {
        'form': form
    })
  
########################################## Delete Model Instance ###############################################

@login_required
def car_delete(request, car_slug):
    car = Car.objects.filter(carSlug = car_slug)
    car.delete()
    #This should hopefully retun the user to the current page refreshed
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
 

@login_required
def system_delete(request, car_slug, system_slug):
    system = System.objects.filter(systemSlug = system_slug)
    system.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def assembly_delete(request, car_slug, system_slug, assembly_slug):
    assembly = Assembly.objects.filter(assemblySlug = assembly_slug)
    assembly.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def part_delete(request, car_slug, system_slug, assembly_slug, part_slug):
    part = Part.objects.filter(partSlug = part_slug)
    part.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def pmft_delete(request, car_slug, system_slug, assembly_slug, part_slug, pmft_slug):
    pmft = PMFT.objects.filter(pmftSlug = pmft_slug)
    pmft.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

  
########################################## Helper Functions ###############################################

def get_user_details(request):
    user_account = UserAccount.objects.get(pk=request.user)
    user_rank = USER_RANKS[user_account.rank]

    return user_account, user_rank

def choosepmft(response):
    if response.method == "POST":
        form = ChoosePmft(response.POST)
        
        if form.is_valid():
            catagory = form.cleaned_data['pmftCatagory']
        
        return HttpResponseRedirect(f'/tool/choosepmft/{catagory}')
        #return redirect(reverse('tool:choosepmft', args=[catagory]))
    else:
        form = ChoosePmft()
        
        return render(response, "tool/choosepmft.html", {"form":form})
    
def individual_process(request,pmfttype,id):
    if pmfttype == "P":
        individualPMFT = IndividualProcess.objects.filter(processCategoryID = id)
        subtype = None
    elif pmfttype == "T":
        individualPMFT = IndividualTool.objects.filter(toolCategoryID = id)
        subtype = None
    context = {
        'individualPMFT': individualPMFT,
        'subtype': subtype,
        'PMFT' : pmfttype,
    }
    return render(request, "tool/process.html" , context)

def pmft_subtype(request,pmfttype):
    mydata = PmftCategory.objects.filter(pmftType = pmfttype)
    context = {
        'pmft_type': mydata,
        'PMFT' : pmfttype
    }
    return render(request, "tool/pmft_subtype.html", context)