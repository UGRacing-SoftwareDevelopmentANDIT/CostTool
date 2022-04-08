from ast import Sub
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import join, slugify
from django.contrib.auth.models import User

#we should consider how deletions should work, cascade or set to null could make quite a difference


class UserAccount(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, primary_key=True)
    # Consider implementing a rank lookup model (instead of hard-coding levels look it up in a model)
    # 2 being the "baseline" for a standard engineer, gives space to implement lower levels.
    rank = models.IntegerField(default=2)

    def __str__(self):
        return self.user.username

      
class Car(models.Model):
    #this will be auto created by conjoining name and year
    carID = models.CharField(max_length=8, unique=True, primary_key=True)
    carName = models.CharField(max_length=10)
    # for simplicity using integerFeild, could implement validation here but given access
    # for higher level users leaving unvalidated
    carYear = models.IntegerField()
    carSlug = models.SlugField(unique = True, default='car-')
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.carSlug = '-'.join((slugify(self.carName), slugify(self.carYear)))
        self.carID = '-'.join((slugify(self.carName), slugify(self.carYear)))
        super(Car, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.carSlug    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['carYear', 'carName'], name='unique_carName_carYear')
    ]
       

class System(models.Model):
    systemID = models.AutoField(primary_key=True)
    systemName = models.CharField(max_length=30)
    carID = models.ForeignKey(Car, on_delete=models.SET_NULL, null = True)
    costed = models.BooleanField(default=False)
    systemSlug = models.SlugField(unique=True, default="system-")
    # subteam = models.ManyToManyField(Subteam)
    def save(self, *args, **kwargs):
        self.systemSlug = '-'.join((slugify(self.systemID), slugify(self.systemName)))
        super(System, self).save(*args, **kwargs)

    def __str__(self):
        return self.systemSlug
   
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['systemName', 'carID'], name='unique_carID_systemName')
        ]
   

class Assembly(models.Model):
    assemblyID = models.AutoField(primary_key=True)
    assemblyName = models.CharField(max_length=30)
    systemID = models.ForeignKey(System, on_delete=models.SET_NULL, null = True)
    assemblyQuantity = models.IntegerField()
    assemblySlug = models.SlugField(unique=True, default="assembly-")
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        # TODO: Need a solution for slugging here
        # slugify(self.assemblyName) will return None, making each slug: none-<self.assemblyName>
        self.assemblySlug = ('-'.join((slugify(self.assemblyID), slugify(self.assemblyName))))
        super(Assembly, self).save(*args, **kwargs)

    def __str__(self):
        return self.assemblySlug

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['assemblyName', 'systemID'], name='unique_assemblyName_systemID')
        ]
   

class Part(models.Model):
    partID = models.AutoField(primary_key=True)
    partName = models.CharField(max_length=15)
    assemblyID = models.ForeignKey(Assembly, on_delete=models.SET_NULL, null = True)
    makeBuy = models.BooleanField()
    #choose validation location for things like 2dp etc
    partCost = models.FloatField(null = True)
    partQuantity = models.IntegerField(default=1)
    partComment = models.CharField(max_length=50, null = True)
    partSlug = models.SlugField(unique=True, default='part-')

    def save(self, *args, **kwargs):
        self.partSlug = '-'.join((slugify(self.partID),slugify(self.partName)))
        super(Part, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.partSlug
    class Meta:
        #additional requirement of parts being unique within systems is also needed
        constraints = [
            models.UniqueConstraint(fields=['partName', 'assemblyID'], name='unique_partName_assemblyID')
        ]
      

class PMFT(models.Model):
    pmftID = models.AutoField(primary_key=True)
    pmftName = models.CharField(max_length=15)
    pmftComment = models.CharField(max_length=50,  null=True)
    pmftCost = models.FloatField(default=0)
    pmftCostComment =  models.CharField(max_length=50,  null=True)
    pmftQuantity = models.IntegerField(default=1)
    partID = models.ForeignKey(Part, on_delete=models.SET_NULL, null = True)
    #a char field must have a max length, when set to 1 it creates an error with the multiple select box, this is a work around
    pmftType = models.CharField(max_length=5)
    pmftSlug = models.SlugField(unique=True, default='pmft-')

    def save(self, *args, **kwargs):
        self.pmftSlug = '-'.join((slugify(self.pmftID),slugify(self.pmftName)))
        super(PMFT, self).save(*args, **kwargs)

    def __str__(self):
        return self.pmftSlug


class Subteam(models.Model):
    teamName = models.CharField(max_length=20, unique=True, primary_key=True)
    abbr = models.CharField(max_length=10, unique=True)
    systems = models.ManyToManyField(System, blank=True)
    subteamSlug = models.SlugField(unique=True, default='team-')

    def save(self, *args, **kwargs):
        self.subteamSlug = (slugify(self.teamName))
        super(Subteam, self).save(*args, **kwargs)

    def __str__(self):
            return self.teamName     


class TeamLinking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    subteam = models.ForeignKey(Subteam, on_delete=models.CASCADE)
    teamHead = models.BooleanField(default=False)          