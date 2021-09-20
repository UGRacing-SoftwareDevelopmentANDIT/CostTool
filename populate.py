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
