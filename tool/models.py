from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import join, slugify
from django.contrib.auth.models import User


#we should consider how deletions should work, cascade or set to null could make quite a difference


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
        super(Car, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug


class System(models.Model):
    systemID = models.AutoField(primary_key=True)
    systemName = models.CharField(max_length=15)
    carID = models.ForeignKey(Car, on_delete=models.SET_NULL, null = True)
    costed = models.BooleanField(default=False)
    systemSlug = models.SlugField(unique=True, default="system-")
    # subteam = models.ManyToManyField(Subteam)
    def save(self, *args, **kwargs):
        self.systemSlug = (slugify(self.systemName))
        super(System, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug


class Assembly(models.Model):
    assemblyID = models.AutoField(primary_key=True)
    assemblyName = models.CharField(max_length=15)
    systemID = models.ForeignKey(System, on_delete=models.SET_NULL, null = True)
    assemblyQuantity = models.IntegerField()
    assemblySlug = models.SlugField(unique=True, default="assembly-")

    def validate_unique(self, exclude = None):
        if Assembly.objects.exclude(assemblyID=self.assemblyID).filter(assemblyName=self.assemblyName, systemID=self.systemID).exists():
            raise ValidationError('There already exists an assembly with that name in this system')
            super(Assembly,self).validate_unique(exclude=exclude)
    
    def save(self, *args, **kwargs):
        # TODO: Need a solution for slugging here
        # slugify(self.assemblyName) will return None, making each slug: none-<self.assemblyName>
        self.assemblySlug = ('-'.join((slugify(self.assemblyID), slugify(self.assemblyName))))
        super(Assembly, self).save(*args, **kwargs)
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
    partSlug = models.SlugField(unique=True, default='part-')

    def save(self, *args, **kwargs):
        self.partSlug = '-'.join((slugify(self.partID),slugify(self.partName)))
        super(Part, self).save(*args, **kwargs)
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
    pmftType = models.CharField(max_length=1)
    pmftSlug = models.SlugField(unique=True, default='pmft-')

    def save(self, *args, **kwargs):
        self.pmftSlug = '-'.join((slugify(self.pmftID),slugify(self.pmftName)))
        super(PMFT, self).save(*args, **kwargs)
        class Meta:
            def __str__(self):
                return self.slug


class UserAccount(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, primary_key=True)
    # Consider implementing a rank lookup model (instead of hard-coding levels look it up in a model)
    # 2 being the "baseline" for a standard engineer, gives space to implement lower levels.
    rank = models.IntegerField(default=2)

    def __str__(self):
        return self.user.username


class Subteam(models.Model):
    teamName = models.CharField(max_length=20, unique=True, primary_key=True)
    abbr = models.CharField(max_length=10, unique=True)
    systems = models.ManyToManyField(System)

    def __str__(self):
        return self.teamName


class TeamLinking(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    subteam = models.ForeignKey(Subteam, on_delete=models.CASCADE)
    teamHead = models.BooleanField(default=False)          