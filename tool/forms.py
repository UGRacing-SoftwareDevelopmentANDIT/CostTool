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


class AddPartForm(forms.ModelForm):
    partName = forms.CharField(max_length=15)
    makeBuy = forms.BooleanField()
    partCost = forms.FloatField(required=False)
    partQuantity = forms.IntegerField()
    partCurrency = forms.CharField(max_length=3, required=False)
    partComment = forms.CharField(max_length=50, required=False)
    partSlug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Part
        fields = ('partName', 'makeBuy', 'partCost', 'partQuantity', 'partCurrency', 'partComment', 'partSlug')