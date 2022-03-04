from django import forms
from django.db.models.expressions import Value
from tool.models import *
from django.contrib.auth.models import User


#have to specify the password field is a PasswordInput so that the password appears hidden on the template
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password',)
 

#the user field is initialised in the views.py file, verified filed is just set to false
class UserAccountForm(forms.ModelForm):
    rank = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    class Meta:
        model = UserAccount
        fields = ('rank',)

        
class CarForm(forms.ModelForm):
    carName = forms.CharField(max_length=20, help_text="Please enter the car name.")
    carYear = forms.CharField(max_length=55, help_text="Please enter the cars year.")
    carSlug = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Car
        fields = ('carName', 'carYear', 'carSlug')

        
class SystemForm(forms.ModelForm):
    systemName = forms.CharField(max_length=20, help_text="Please enter the system name.")
    costed = forms.BooleanField(help_text="Please check if the system is costed.", required=False)
    systemSlug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = System
        fields = ('systemName', 'costed', 'systemSlug')  


class AssemblyForm(forms.ModelForm):
    assemblyName = forms.CharField(max_length=15)
    assemblyQuantity = forms.IntegerField()
    assemblySlug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Assembly
        fields = ('assemblyName', 'assemblyQuantity',)


class PartForm(forms.ModelForm):
    partName = forms.CharField(max_length=15)
    makeBuy = forms.BooleanField()
    partCost = forms.FloatField(required=False)
    partQuantity = forms.IntegerField()
    partComment = forms.CharField(max_length=50, required=False)
    partSlug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Part
        fields = ('partName', 'makeBuy', 'partCost', 'partQuantity', 'partComment', 'partSlug')


class PMFTForm(forms.ModelForm):
    pmftName = forms.CharField(max_length=15)
    pmftComment = forms.CharField(max_length=50,  required=False)
    pmftCost = forms.FloatField()
    pmftCostComment =  forms.CharField(max_length=50,  required=False)
    pmftQuantity = forms.IntegerField()
    pmftType = forms.CharField(max_length=1)
    pmftSlug = forms.SlugField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = PMFT
        fields = ('pmftName', 'pmftComment', 'pmftCost', 'pmftCostComment', 'pmftQuantity', 'pmftType', 'pmftSlug')

class EditSubteam(forms.ModelForm):
    subteamQ = forms.ModelChoiceField(queryset=Subteam.objects.all().order_by('teamName'),required=True)

    class Meta:
        model = Subteam
        fields = ('subteamQ',)


class EditAssignEng(forms.ModelForm):
    engineer = forms.ModelChoiceField(queryset=UserAccount.objects.all(), required=True)

    class Meta:
        model = Assembly
        fields = ('engineer',)
