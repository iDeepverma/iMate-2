from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            messages.success(request, f'Account created for {request.user.username}!!!')
            return redirect('profile')
    context['form'] = form
    return render(request, 'accounts/signup.html',context)

def loginView(request):
    # if request.user.is_authenticated():
    #     return redirect('chat-recent')
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
				messages.error(request,f'Invalid username or password.')
		else:
			messages.error(request,f'Invalid username or password.')
	form = AuthenticationForm()
	return render(request=request, template_name="accounts/login.html", context={"form":form})

@login_required
def logoutView(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('login')

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
            messages.success(request , f'Account updated!',extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('chat-recent')
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

# def searchView(request,username):
#     if request.user.username == username:
#         return redirect('profile')
#     else:
#         context = {}
#         context['profile'] =  get_object_or_404(get_user_model(),username=username).profile
#         return render(request,'accounts/search.html')

def about(request):
    return render(request,'about.html')