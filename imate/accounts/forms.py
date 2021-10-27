from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import fields
from . import models
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
            userProfile = models.UserProfile(user=newUser, userHash = userHash)
            userProfile.save()
        return newUser
