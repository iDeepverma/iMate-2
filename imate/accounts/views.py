from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from . import forms
# Create your views here.

def signupView(request):
    context = {}
    form  = forms.SignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('login')
    context['form'] = form
    return render(request, 'accounts/signup.html',context)

def loginView(request):
    pass

def logoutView(request):
    pass