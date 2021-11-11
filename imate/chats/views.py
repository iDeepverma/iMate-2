from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import get_user_model
from . import models as chat_models
from accounts.models import UserProfile
# Create your views here.
 
def chatView(request,username=None):
    if request.user.is_authenticated:
        context = {}
        profile = UserProfile.objects.get(user=request.user) #PROFILE OF LOGGED IN USER
        friendlist = profile.userFriends.all() #frnd of current logged in user
        recents = []    #for the side contact list
        for i in friendlist:
            chatHash = chat_models.conversastionhash(request.user, i)
            msgs = chat_models.Message.objects.filter(userHash=chatHash)
            unread = len(msgs.filter(isRead=False))
            try :
                lastMsg = msgs.latest('timestamp').message
            except :
                lastMsg =""
 
            recentData = {
                'frnd':i,
                'unread':unread, #no of unread
                'lastMsg':lastMsg #lastmsg
            }
            recents.append(recentData)
        # recents.sort(reverse=True,key=lambda a: a['lastMsg'].timestamp)
        context['recents'] = recents
        # try:
        #     activeFrnd = get_user_model().get(username =  username)
        # except get_user_model().DoesNotExist:
        #     # error handling if no such username exits
        if username !=None:
            context['activeFrnd'] = get_object_or_404(get_user_model(),username=username) #current-convo-open
            convHash = chat_models.conversastionhash(request.user,context['activeFrnd'])
            context['activeFrndMsgs'] = chat_models.Message.objects.filter(userHash=convHash).order_by('-timestamp')
            context['activeFrndProfile'] = context['activeFrnd'].profile
        else:
            context['activeFrnd']=None
            context['activeFrndMsgs']=None
            context['activeFrndProfile'] = None
 
        return render(request,'chats/main-chat-page2.html',context)
 
    else :
        return redirect('login')
 
 
# def recentChat(request):
#     context = {}
#     profile = UserProfile.objects.get(user=request.user)
#     friendlist = profile.userFriends.all()
#     recents = []
#     for i in friendlist:
#         chatHash = chat_models.conversastionhash(request.user, i)
#         msgs = chat_models.Message.objects.filter(userHash=chatHash)
#         unread = len(msgs.filter(isRead=False))
#         lastMsg = msgs.latest('timestamp')
#         recentData = {
#             'unread':unread,
#             'lastMsg':lastMsg,
#             'frnd':i
#         }
#         recents.append(recentData)
#     context['recents'] = recents
 
#     return render(request,'chats/recent-chats.html',context)
 