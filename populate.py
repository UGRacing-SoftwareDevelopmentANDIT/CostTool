import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'costing-web-app.settings')

import django

django.setup()
from django.core.files import File
from tool.models import UserAccount
from datetime import datetime
from pytz import utc
from django.contrib.auth.models import User

'''
def populate():
    userInfo = [
         {'user': 'Amanda',
          'email': 'Amanda99@gmail.com',
          'password': 'AmandaPass1',
          'verified': False},
         {'user': 'Charlie',
         'email': 'Charlie66@gmail.com',
          'password': 'CharliePass2098',
          'verified': True},
         {'user': 'lifehackfan',
         'email': 'lifehackfan@gmail.com',
          'password': 'passThis69',
          'verified': False},
         {'user': 'jasper999',
         'email': 'jasper999@gmail.com',
          'password': 'weflknlkqcnkq',
          'verified': True},
         {'user': 'davidf99',
         'email': 'davidf99@gmail.com',
          'password': 'notMyPass420',
          'verified': True}]
    userAccounts = []
    for info in userInfo:
        userAccounts.append(AddUserAccount(info['user'], info['email'], info['password'], info['verified']))
'''


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
        c= add_car(car['carID'],car['carName'], car['carYear'])
        Car.append(c)

    systeminfo = [
         {
          'systemName': 'ELECTRICAL',   
          'carID': 'Test2021',
          'costed': True
          }
         ]
    System = []
    for system in systeminfo:
        s=add_system(system['systemName'],c, system['costed'])
        System.append(s)

    assemblyinfo = [
         {
          'assemblyName': 'Test 1',   
          'assemblyQuantity': 10
          }
         ]
    Assembly = []
    for assembly in assemblyinfo:
        a=add_assembly(assembly['assemblyName'],s, assembly['assemblyQuantity'])
        Assembly.append(a)

    partinfo = [
         {
          'partName': 'Test part 12',
          'makeBuy': True ,
          'partCost': 120 ,
          'partQuantity': 6,
          'partCurrency': 'EUR',
          'partComment': 'This is a comment'
          }
         ]
    Part = []
    for part in partinfo:
        p=add_part(part['partName'],a, part['makeBuy'], part['partCost'], part['partQuantity'], part['partCurrency'], part['partComment'])
        Part.append(p)

    pmftinfo = [
         {
          'pmftName': 'test',
          'pmftComment': 'this is a comment',
          'pmftCost': 60,
          'pmftCurrency': 'EUR',
          'pmftCostComment': 'This is a cost commemt',
          'pmftQuantity': 8,
          'pmftType': 'M'
          }
         ]
    PMFT = []
    for pmft in pmftinfo:
        pm=add_pmft(pmft['pmftName'],pmft['pmftComment'],pmft['pmftCost'],pmft['pmftCurrency'],pmft['pmftCostComment'],pmft['pmftQuantity'],p,pmft['pmftType'])
        PMFT.append(pm)


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

def add_part(partName,assemblyID,makeBuy,partCost,partQuantity,partCurrency,partComment):

    p = Part.objects.get_or_create(partName=partName,assemblyID=assemblyID, makeBuy=makeBuy,partCost=partCost,partQuantity=partQuantity,partCurrency=partCurrency,partComment=partComment)[0]
    p.partName = partName
    p.assemblyID = assemblyID
    p.makeBuy = makeBuy
    p.partCost =partCost
    p.partQuantity = partQuantity
    p.partCurrency = partCurrency
    p.partComment = partComment
    p.save()

    return p

def add_pmft(pmftName,pmftComment,pmftCost,pmftCurrency,pmftCostComment,pmftQuantity,partID,pmftType):

    pm = PMFT.objects.get_or_create(pmftName=pmftName,pmftComment=pmftComment, pmftCost=pmftCost,pmftCurrency=pmftCurrency,pmftCostComment=pmftCostComment,pmftQuantity=pmftQuantity,partID=partID,pmftType=pmftType)[0]
    pm.pmftName = pmftName
    pm.pmftComment = pmftComment
    pm.pmftCost = pmftCost
    pm.pmftCurrency =pmftCurrency
    pm.pmftCostComment = pmftCostComment
    pm.partID = partID
    pm.pmftType = pmftType
    pm.save()

    return pm




if __name__ == '__main__':
    print('Starting population script...')
    populate()



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


if __name__ == '__main__':
    print('Starting population script...')
    populate()
