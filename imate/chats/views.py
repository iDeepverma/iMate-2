from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import get_user_model
from . import models as chat_models
from accounts.models import UserProfile,RandomFrnd
from django.contrib.auth.decorators import login_required
from django.http import Http404
from . import randomFill
import time
# Create your views here.
 

@login_required
def chatView(request,username=None):
    context = {}
    profile = UserProfile.objects.get(user=request.user) #PROFILE OF LOGGED IN USER
    friendlist = profile.userFriends.all() #frnd of current logged in user
    recents = []    #for the side contact list
    for i in friendlist:
        chatHash = chat_models.conversastionhash(request.user, i)
        msgs = chat_models.Message.objects.filter(userHash=chatHash)
        unread = len(msgs.filter(isRead=False))
        try :
            lastMsgObj = msgs.latest('timestamp')
            lastMsg = lastMsgObj.message
            isYou = True if lastMsgObj.sender==request.user else False
        except :
            lastMsg =""
            isYou = False

        recentData = {
            'frnd':i,
            'unread':unread, #no of unread
            'lastMsg':lastMsg, #laSstmsg
            'isYou':isYou
        }
        recents.append(recentData)
    context['recents'] = recents

    if username !=None:
        context['activeFrnd'] = get_object_or_404(get_user_model(),username=username) #current-convo-open
        
        if context['activeFrnd'] not in friendlist:                                   #checking if requested frnd is in frndlist 
            raise Http404
        
        convHash = chat_models.conversastionhash(request.user,context['activeFrnd'])
        context['activeFrndMsgs'] = chat_models.Message.objects.filter(userHash=convHash).order_by('timestamp')
        context['activeFrndProfile'] = context['activeFrnd'].profile
    else:
        context['activeFrnd']=None
        context['activeFrndMsgs']=None
        context['activeFrndProfile'] = None

    return render(request,'chats/main-chat-page2.html',context)
 

@login_required
def randomWaiting(request):
    return render(request,'chats/waiting.html')

@login_required
def randomChatting(request):
    context = {
        'chatId' : request.user.profile.randomChatId,
        'randomAlias' : randomFill.randNamefn()
    }
    return render(request,'chats/randomChat.html',context)

@login_required
def addFriend(request):
    obj = RandomFrnd.objects.get(chatHash=request.user.profile.randomChatId)
    if request.user.profile == obj.user1:
        print('ONe')
        obj.user1consent = True
        obj.save()
    elif request.user.profile == obj.user2:
        print('Two')
        obj.user2consent = True
        obj.save()
    if obj.user1consent and obj.user2consent:
        print("Done")
        obj.user1.userFriends.add(obj.user2.user)
        obj.user2.userFriends.add(obj.user1.user)
        obj.delete()
    # messages.success(request,'Sent Request')
    return redirect('chat-recent')