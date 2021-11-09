from django.shortcuts import render
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from . import forms
from . import models
import hashlib
# Create your views here.

def signupView(request):
    context = {}
    form  = forms.SignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
    context['form'] = form
    return render(request, 'accounts/signup.html',context)

def loginView(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="accounts/login.html", context={"form":form})

@login_required
def logoutView(request):
    logout(request)
    return render(request,'accounts/logout.html')

# @login_required
# def profileView(request):
#     try:
#         profile = request.user.profile
#     except get_user_model().profile.RelatedObjectDoesNotExist:
#         profile = models.UserProfile.objects.create(user = request.user, userHash = hashlib.sha256(request.user.username.encode()).hexdigest())
#     return render(request,'accounts/profile.html',{'profile':profile})


@login_required
def profileView(request):
    if request.method =='POST':
        u_form = forms.UserUpdateForm(request.POST,instance = request.user)
        p_form = forms.ProfileUpdateForm( request.POST,
                                    request.FILES,
                                    instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request , f'Account updated!')
            return redirect('profile')
    else :
        try:
            UserProfile = request.user.profile
        except:
            UserProfile = models.UserProfile.objects.create(user=request.user)

        u_form = forms.UserUpdateForm(instance = request.user)
        p_form = forms.ProfileUpdateForm(instance = UserProfile)
        context = {
            'u_form' : u_form,
            'p_form' : p_form
        }
    return render(request, 'accounts/profile.html', context)