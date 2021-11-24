# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<frnd_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/waiting/$',consumers.RandomChatPairer.as_asgi()),
    re_path(r'ws/randomChat/$',consumers.RandomChat.as_asgi()),
]