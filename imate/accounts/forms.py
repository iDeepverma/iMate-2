from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import fields
from django import forms
from .models import UserProfile
import hashlib

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username','email','password1','password2')
    
    def save(self, commit=True):
        newUser = super(SignupForm,self).save(commit=False)
        newUser.email = self.cleaned_data['email']
        if commit == True:
            newUser.save()
            userHash = hashlib.sha256(newUser.username.encode()).hexdigest()
            userProfile = UserProfile(user=newUser, userHash = userHash)
            userProfile.save()
        return newUser

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['userPic' , 'userBio' ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
