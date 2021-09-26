from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


"""
UserAccount model has 2 fields:
user which implements the django user interface and is pimary key and cascades on dellete
verified which is a boolean value used to keep track whether a suer is verified and has acces to certain features of the webapp
"""


class UserAccount(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, primary_key=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Car(models.Model):
    #this will be auto created by conjoining name and year
    carID = models.CharField(max_length=8, unique=True, primary_key=True)
    carName = models.CharField(max_length=4)
    # for simplicity using integerFeild, could implement validation here but given access
    # for higher level users leaving unvalidated
    carYear = models.IntegerField()

    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug

class System(models.Model):
    systemID = models.AutoField(primary_key=True)
    systemName = models.CharField(unique=True, max_length=15)
    CarID = models.ForeignKey(Car, on_delete=models.SET_NULL, null = True)
    Costed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug

class Assembly(models.Model):
    assemblyID = models.AutoField(primary_key=True)
    assemblyName = models.CharField(unique=True, max_length=15)
    systemID = models.ForeignKey(System, on_delete=models.SET_NULL, null = True)
    assemblyQuantity = models.IntegerField()
    
    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug
class Part(models.Model):
    partID = models.AutoField(primary_key=True)
    partName = models.CharField(max_length=15)
    assemblyID = models.ForeignKey(Assembly, on_delete=models.SET_NULL, null = True)
    makeBuy = models.BooleanField()
    #choose validation location for things like 2dp etc
    partCost = models.FloatField(null = True)
    partQuantity = models.IntegerField(default=1)
    partCurrency = models.CharField(max_length=3, null = True)
    partComment = models.CharField(max_length=50, null = True)

    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug
class PMFT(models.Model):
    pmftID = models.AutoField(primary_key=True)
    pmftName = models.CharField(max_length=15)
    pmftComment = models.CharField(max_length=50,  null=True)
    pmftCost = models.FloatField(default=0)
    pmftCurrency = models.CharField(max_length=3, null = True)
    pmftCostComment =  models.CharField(max_length=50,  null=True)
    pmftQuantity = models.IntegerField(default=1)
    partID = models.ForeignKey(Part, on_delete=models.SET_NULL, null = True)
    partType = models.CharField(max_length=1)

    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug