from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatHomeRedirect , name ='chat-home'),
    path('chat/<slug:username>/',views.chatView, name='chat-page'),
]
