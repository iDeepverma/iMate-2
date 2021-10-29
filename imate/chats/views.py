from django.shortcuts import render,get_object_or_404
from django.contrib.auth import get_user_model
from . import models
# Create your views here.

def chatView(request,username):
    # try:
    #     frnd = get_user_model().get(username =  username)
    # except get_user_model().DoesNotExist:
    #     # error handling if no such username exits
    context = {}
    context['frnd'] = get_object_or_404(get_user_model(),username=username)
    convHash = models.conversastionhash(request.user,context['frnd'])
    context['messages'] = models.Message.objects.filter(userHash=convHash).order_by('-timestamp')
    context['frndProfile'] = context['frnd'].profile

    return render(request,'chats/main-chat-page.html',context)
    
    
