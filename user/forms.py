from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput
from django import forms

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username': TextInput(attrs={'class':'form-control valid','placeholder':'username'}),
            'email': EmailInput(attrs={'class': 'form-control valid', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'name'}),
            'last_name': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'surname'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','address','image')
        widgets = {
            'phone': TextInput(attrs={'class':'form-control valid', 'placeholder': 'username'}),
            'address': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'email'}),
            'image': FileInput(attrs={'class': 'form-control valid'}),
        }
