from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatView , name ='chat-recent'),
    path('chat/<slug:username>/',views.chatView, name='chat-page'),
    path('waiting/',views.randomWaiting,name='waiting'),
    path('random/',views.randomChatting,name='randomChat'),
    path('addfrnd/',views.addFriend,name='addfrnd')
]
