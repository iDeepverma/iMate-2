import json
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated == False:
            raise DenyConnection('User not logged in')
        self.groupName = await database_sync_to_async(self.getGroupName)()
        self.friendGroup = await database_sync_to_async(self.getFriendGroup)()

        await self.channel_layer.group_add(
            self.groupName,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.friendGroup,
            self.channel_name
        )

        return await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.groupName,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.friendGroup,
            self.channel_name
        )
        return await super().disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        data_obj = json.loads(text_data)
        message = data_obj['message']
        await database_sync_to_async(self.addMessage)(message)
        # await self.channel_layer.group_send(
        #     self.groupName,
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         'sender':self.user.username,
        #         'receiver':self.friend.username
        #     }
        # )
        await self.channel_layer.group_send(
            self.friendGroup,
            {
                'type': 'chat_message',
                'message': message,
                'sender':self.user.username,
                'receiver':self.friend.username
            }
        )
        return await super().receive(text_data=text_data, bytes_data=bytes_data)
    
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'sender':self.user.username,
                'receiver':self.friend.username
        }))
    
    def getGroupName(self):
        self.profile = self.user.profile
        return self.profile.userHash
    
    def getFriendGroup(self):
        self.friend = get_object_or_404(get_user_model(),username=self.scope['url_route']['kwargs']['frnd_name'])
        return self.friend.profile.userHash
    
    def addMessage(self,message):
        models.Message.objects.create(sender=self.user, receiver=self.friend, message=message)

