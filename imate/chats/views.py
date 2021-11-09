from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import get_user_model
from . import models
from accounts.models import UserProfile
# Create your views here.

def chatView(request,username=None):
    if user.is_authenticated:
        context = {}
        profile = UserProfile.objects.get(user=request.user)
        friendlist = profile.userFriends.all()
        recents = []
        for i in friendlist:
            chatHash = models.conversastionhash(request.user, i)
            msgs = models.Message.objects.filter(userHash=chatHash)
            unread = len(msgs.filter(isRead=False))
            msg = msgs.latest('timestamp')
            recentData = {
                'unread':unread,
                'msg':msg,
                'friendName':i
            }
            recents.append(recentData)
        context['recents'] = recents
        # try:
        #     frnd = get_user_model().get(username =  username)
        # except get_user_model().DoesNotExist:
        #     # error handling if no such username exits
        if username !=None:
            context['frnd'] = get_object_or_404(get_user_model(),username=username)
            convHash = models.conversastionhash(request.user,context['frnd'])
            context['messages'] = models.Message.objects.filter(userHash=convHash).order_by('-timestamp')
            context['frndProfile'] = context['frnd'].profile
        else:
            context['frnd']=None
            context['messages']=None
            context['frndProfile'] = None

        return render(request,'chats/main-chat-page.html',context)
    
    else :
        return redirect('login')


# def recentChat(request):
#     context = {}
#     profile = UserProfile.objects.get(user=request.user)
#     friendlist = profile.userFriends.all()
#     recents = []
#     for i in friendlist:
#         chatHash = models.conversastionhash(request.user, i)
#         msgs = models.Message.objects.filter(userHash=chatHash)
#         unread = len(msgs.filter(isRead=False))
#         msg = msgs.latest('timestamp')
#         recentData = {
#             'unread':unread,
#             'msg':msg,
#             'friendName':i
#         }
#         recents.append(recentData)
#     context['recents'] = recents

#     return render(request,'chats/recent-chats.html',context)

    

