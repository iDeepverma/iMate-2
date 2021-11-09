from django.urls import path
from . import views

urlpatterns = [
    path('chat/<slug:username>/',views.chatView, name='chat-page'),
    path('chat/',views.chatView,name='recent'),
]
