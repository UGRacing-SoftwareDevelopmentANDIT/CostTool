import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'costing-web-app.settings')

import django

django.setup()
from django.core.files import File
from tool.models import *
from django.contrib.auth.models import User

#from datetime import datetime
#from pytz import utc



def populate():
    carinfo = [
         {
          'carID': 'Test2021',   
          'carName': 'Test',
          'carYear': '2021'
          }
         ]
    Car = []
    for car in carinfo:
        Car.append(add_car(car['carID'],car['carName'], car['carYear']))


def AddUserAccount(userName, email, pword, verified):
    user=User.objects.create_user(userName, email=email, password=pword)
    user.is_superuser=True
    user.is_staff=True
    user.save()
    u = UserAccount.objects.get_or_create(user=user, verified=verified)[0]
    u.user = user
    u.verified = verified
    u.save()
    return u

def add_car(carID,carName,carYear):


    c = Car.objects.get_or_create(carID=carID,carName=carName, carYear=carYear)[0]
    c.carName = carName
    c.carYear = carYear
    c.save()

    return c

def add_system(systemName,Costed):

    pass

    return 0

def add_assembly(assemblyName, assemblyQuantity):

    pass

    return 0

def add_part(partName,makeBuy,partCost,partQuantity,partCurrency,partComment):

    pass

    return 0

def add_pmft(pmftName,pmftComment,pmftCost,pmftCurrency,pmftCostComment,pmftQuantity,partType):

    pass

    return 0




if __name__ == '__main__':
    print('Starting population script...')
    populate()
