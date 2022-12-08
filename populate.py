import os
import string
import random
import csv


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'costing-web-app.settings')

import django

django.setup()
from django.core.files import File
from django.db.models import Q
from tool.models import *
from datetime import datetime
from pytz import utc
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

def populate():
    '''# Add Admins
    userInfoAdmins = [
        "REDACTED"
    ]
    
    for user in userInfoAdmins:
        AddUserAccount(user['user'], user['email'], user['password'], is_staff=True, is_superuser=True, rank=4)
        userAccounts.append([user['user'], user['password']])

    # Add Cost Heads
    userInfoCostHeads = [
        "REDACTED"
    ]
    for user in userInfoCostHeads:
        AddUserAccount(user['user'], user['email'], user['password'], is_staff=False, is_superuser=False, rank=4)
        userAccounts.append([user['user'], user['password']])
    '''
    userAccounts = []
    # Add Engineers
    user_engineers, eng_allocs = import_engineers("import_engineers.csv")
    added_users = []
    for user in user_engineers:
        if user['user'] not in added_users:
            AddUserAccount(user['user'], user['email'], user['password'])
            userAccounts.append([user['user'], user['password']])
            added_users.append(user["user"])

    # Car Populate
    carinfo = [
        {
            'carID': 'IC2022',   
            'carName': 'UGR22 IC',
            'carYear': '2022'
        }
    ]
    Car = []
    for car in carinfo:
        c= add_car(car['carID'],car['carName'], car['carYear'])
        Car.append(c)

    # System Populate
    systeminfo = [
        {
            'systemName': 'Brakes',   
            'carID': 'IC2022',
            'costed': False
        },
        {
            'systemName': 'Powertrain',   
            'carID': 'IC2022',
            'costed': True
        },
        {
            'systemName': 'Frame and Body',   
            'carID': 'IC2022',
            'costed': True
        },
        {
            'systemName': 'Electrical',   
            'carID': 'IC2022',
            'costed': False
        },
        {
            'systemName': 'Miscellanous',   
            'carID': 'IC2022',
            'costed': False
        },
        {
            'systemName': 'Steering System',   
            'carID': 'IC2022',
            'costed': False
        },
        {
            'systemName': 'Suspension',   
            'carID': 'IC2022',
            'costed': False
        },
        {
            'systemName': 'Wheels',   
            'carID': 'IC2022',
            'costed': False
        },
    ]
    for system in systeminfo:
        s=add_system(system['systemName'], c, system['costed'])

    # Assembly Populate
    assemblyinfo = [
        {
            'assemblyName': 'Test 1',   
            'assemblyQuantity': 10
        }
    ]
    Assembly = []
    for assembly in assemblyinfo:
        a=add_assembly(assembly['assemblyName'], s, assembly['assemblyQuantity'])
        Assembly.append(a)

    # Part Populate
    partinfo = [
        {
            'partName': 'Test part 12',
            'makeBuy': True ,
            'partCost': 120 ,
            'partQuantity': 6,
            'partComment': 'This is a comment'
        }
    ]
    Part = []
    for part in partinfo:
        p=add_part(part['partName'], a, part['makeBuy'], part['partCost'], part['partQuantity'], part['partComment'])
        Part.append(p)

    # PMFT Populate
    pmftinfo = [
        {
            'pmftName': 'test',
            'pmftComment': 'this is a comment',
            'pmftCost': 60,
            'pmftCostComment': 'This is a cost commemt',
            'pmftQuantity': 8,
            'pmftType': 'M'
        }
    ]
    PMFT = []
    for pmft in pmftinfo:
        pm=add_pmft(pmft['pmftName'],pmft['pmftComment'],pmft['pmftCost'],pmft['pmftCostComment'],pmft['pmftQuantity'],p,pmft['pmftType'])
        PMFT.append(pm)

    # Add Subteams
    subteam_info = [
        {
            'teamName': 'Electrical',
            'abbr': 'EL',
            'systems': System.objects.get(systemName="Electrical"),
        },
        {
            'teamName': 'Brakes',
            'abbr': 'BR',
            'systems': System.objects.get(systemName="Brakes"),
        },
        {
            'teamName': 'Powertrain',
            'abbr': 'ED',
            'systems': System.objects.get(systemName="Powertrain"),
        },
        {
            'teamName': 'Frame and Body',
            'abbr': 'FR',
            'systems': System.objects.get(systemName="Frame and Body"),
        },
        {
            'teamName': 'Miscellanous',
            'abbr': 'MS',
            'systems': System.objects.get(systemName="Miscellanous"),
        },
        {
            'teamName': 'Steering System',
            'abbr': 'ST',
            'systems': System.objects.get(systemName="Steering System"),
        },
        {
            'teamName': 'Suspension',
            'abbr': 'SU',
            'systems': System.objects.get(systemName="Suspension"),
        },
        {
            'teamName': 'Wheels',
            'abbr': 'WT',
            'systems': System.objects.get(systemName="Wheels"),
        },
    ]
    for subteam in subteam_info:
        st = add_subteam(subteam["teamName"], subteam["abbr"], subteam["systems"])

    # Add Engineers to Subteams
    teamlinking_info = [{
        'user':UserAccount.objects.get(user=User.objects.get(username=eng_alloc["user"])),
        'subteam':Subteam.objects.get(teamName=eng_alloc["subteam"]),
        'teamHead':eng_alloc["teamHead"],
    } for eng_alloc in eng_allocs]

    TeamLinking = []
    for teamlinking in teamlinking_info:
        tl = add_team_linking(teamlinking["user"], teamlinking["subteam"], teamlinking["teamHead"])
        TeamLinking.append(tl)

    # Finish Populate
    export_users(userAccounts, "user_export.csv")


# Helper Functions
# Model Helper Functions
def add_user(userName, email, pword, is_staff, is_superuser):
    try:
        user = User.objects.get_or_create(username=userName, email=email, password=pword)[0]
    except IntegrityError:
        user = User.objects.get(username=userName)
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.save()
    return user


def AddUserAccount(userName, email, pword, is_staff=False, is_superuser=False, rank=2):
    user = add_user(userName, email, pword, is_staff, is_superuser)
    try:
        u = UserAccount.objects.create(user=user, rank=rank)
        u.user = user
    except IntegrityError:
        u = UserAccount.objects.get(user=user)
    u.save()
    
    return u

def add_car(carID,carName,carYear):
    print('#######')
    try:
        c = Car.objects.get(carName=carName, carYear=carYear)
    except Car.DoesNotExist:
        c = Car.objects.create(carID=carID,carName=carName, carYear=carYear)
    c.carName = carName
    c.carYear = carYear
    c.save()

    return c


def add_system(systemName,carID,costed):
    s = System.objects.get_or_create(systemName=systemName,carID=carID, costed=costed)[0]
    s.systemName = systemName
    s.carID = carID
    s.costed = costed
    s.save()

    return s


def add_assembly(assemblyName,systemID,assemblyQuantity):
    a = Assembly.objects.get_or_create(assemblyName=assemblyName,systemID=systemID, assemblyQuantity=assemblyQuantity)[0]
    a.assemblyName = assemblyName
    a.systemID = systemID
    a.assemblyQuantity = assemblyQuantity
    a.save()

    return a


def add_part(partName,assemblyID,makeBuy,partCost,partQuantity,partComment):
    p = Part.objects.get_or_create(partName=partName,assemblyID=assemblyID, makeBuy=makeBuy,partCost=partCost,partQuantity=partQuantity,partComment=partComment)[0]
    p.partName = partName
    p.assemblyID = assemblyID
    p.makeBuy = makeBuy
    p.partCost =partCost
    p.partQuantity = partQuantity
    p.partComment = partComment
    p.save()

    return p


def add_pmft(pmftName,pmftComment,pmftCost,pmftCostComment,pmftQuantity,partID,pmftType):
    pm = PMFT.objects.get_or_create(pmftName=pmftName,pmftComment=pmftComment, pmftCost=pmftCost, pmftCostComment=pmftCostComment,pmftQuantity=pmftQuantity,partID=partID,pmftType=pmftType)[0]
    pm.pmftName = pmftName
    pm.pmftComment = pmftComment
    pm.pmftCost = pmftCost

    pm.pmftCostComment = pmftCostComment
    pm.partID = partID
    pm.pmftType = pmftType
    pm.save()

    return pm


def add_subteam(teamName, abbr, systems):
    st = Subteam.objects.get_or_create(teamName=teamName, abbr=abbr)[0]
    st.teamName = teamName
    st.abbr = abbr
    st.systems.add(systems)
    
    st.save()

    return st


def add_team_linking(user, subteam, teamHead=False):
    tl = TeamLinking.objects.get_or_create(user=user, subteam=subteam, teamHead=teamHead)[0]
    tl.user = user
    tl.subteam = subteam
    tl.teamHead = teamHead   
    
    tl.save()

    return tl


# General Helper Functions
def generate_random_pass():
    characters = string.ascii_letters + string.digits + string.punctuation
    out_pass = "".join(random.choice(characters) for i in range(12))
    return out_pass


def import_engineers(filename):
    engineers = []
    eng_allocs = []

    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            engineer = {}
            engineer["user"] = f"{row[0].split()[0]}_{row[0].split()[-1]}"
            engineer["email"] = row[1]
            engineer["password"] = generate_random_pass()
            engineers.append(engineer)

            ea = {}
            ea["user"] = engineer["user"]
            ea["subteam"] = row[2]
            ea["teamHead"] = True if row[3] == "1" else False
            eng_allocs.append(ea)

    return engineers, eng_allocs


def export_users(userAccounts, output_filename):
    with open(output_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(userAccounts)


if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Completed population script, exiting...')
