from django import forms
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
    verified = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserAccount
        fields = ('verified',)

class AddCarForm(forms.ModelForm):
    carName = forms.CharField(max_length=20, help_text="Please enter the car name.")
    carYear = forms.CharField(max_length=55, help_text="Please enter the cars year.")
    carSlug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Car
        fields = ('carName', 'carYear', 'carSlug')     

class AddSystemForm(forms.ModelForm):
    systemID = forms.CharField(max_length=20, help_text="Please enter the system ID.")
    systemName = forms.CharField(max_length=20, help_text="Please enter the system name.")
    carID = forms.CharField(max_length=20, help_text="Please enter the car ID.")
    costed = forms.BooleanField(help_text="Please check if the system is costed.")
    systemSlug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = System
        fields = ('systemID', 'systemName', 'carID', 'costed', 'systemSlug')  