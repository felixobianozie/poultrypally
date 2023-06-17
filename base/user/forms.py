from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from base.models import CustomUser, Farm


class LoginForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'w3-input w3-round'}),
            'password': forms.TextInput(attrs={'class': 'w3-input w3-round'}),
        } 


class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w3-input w3-round', 'required': True}), label="Password"
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w3-input w3-round', 'required': True}), label="Password Confirmation"
        )

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password1', 'password2', 'pix')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-round'}), 
            'email': forms.TextInput(attrs={'class': 'w3-input w3-round'}),  
            'pix': forms.ClearableFileInput(attrs={'class': 'w3-input w3-round'})}
        labels = {
            'pix': 'Profile Pix'
        }


class FarmForm(ModelForm):
    class Meta:
        model = Farm
        fields = ('name', 'address',)
        labels = {'name': 'Farm Name',
            'address': 'Farm Address'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }