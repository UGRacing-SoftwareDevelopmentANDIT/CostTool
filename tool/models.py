from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


"""
UserAccount model has 2 fields: 
user which implements the django user interface and is pimary key and cascades on dellete
verified which is a boolean value used to keep track whether a suer is verified and has acces to certain features of the webapp
"""
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True, primary_key=True)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username