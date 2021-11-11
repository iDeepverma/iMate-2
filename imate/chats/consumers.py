import json,random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.exceptions import DenyConnection
from . import models
from accounts.models import RandomChat, UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        #Run when client connect to server via a websoclet
        self.user = self.scope['user']
        if self.user.is_authenticated == False:
            raise DenyConnection('User not logged in')
        
        self.groupName = await database_sync_to_async(self.getGroupName)()     #derives groupname for the user
        self.friendGroup = await database_sync_to_async(self.getFriendGroup)() #derives groupname for the recipent,i.e friend
        await database_sync_to_async(self.setOnline)(True)                     #sets its online status to true

        await self.channel_layer.group_add(                                    #adding channel layer to above two groups
            self.groupName,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.friendGroup,
            self.channel_name
        )

        return await self.accept()

    async def disconnect(self, code):                                          #run when websocket closes 
        await self.channel_layer.group_discard(                                #removes channel name from above two groups
            self.groupName,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.friendGroup,
            self.channel_name
        )
        await database_sync_to_async(self.setOnline)(False)                    #sets online status to false in profile database
        
        return await super().disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        '''
            Gets events from the clients via the websocket.
            the type field in the text_data chooses which handler to run for that specific event
        '''

        data_obj = json.loads(text_data)
        message = data_obj['message']                                          #raw message from the websocket
        msg = await database_sync_to_async(self.addMessage)(message)           #message object added to our model
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
                'receiver':self.friend.username,
                # 'time': msg.timestamp
            }
        )

        onlineStatus = await database_sync_to_async(self.getOnline)()

        await self.send(text_data=json.dumps({
                'type':'status_update',
                'value':onlineStatus
        }))

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
        msg = models.Message.objects.create(sender=self.user, receiver=self.friend, message=message)
        return msg
    
    def setOnline(self, value):
        profile = UserProfile.objects.get(user=self.user)
        profile.isOnline = value
        profile.save()
    
    def getOnline(self):
        onlineStatus=UserProfile.objects.get(user=self.friend).isOnline
        return onlineStatus

class RandomChatPairer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated == False:
            raise DenyConnection('User not logged in')
        randomChatid = await database_sync_to_async(self.addRandomChat)()
        return await self.accept()
    
    async def disconnect(self, code):
        await database_sync_to_async(self.removeRandomChat)()
        return await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        if message=='search':
            pair = await database_sync_to_async(self.getPair)()
            if pair == None:
                await self.send(text_data=json.dumps({
                    'type':'info',
                    'pair_status':False
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type':'info',
                    'pair_status':True,
                    'pair_code':pair
                }))


        return await super().receive(text_data=text_data, bytes_data=bytes_data)

    def addRandomChat(self):
        return RandomChat.objects.get_or_create(user=self.user)

    def getPair(self):
        peopleList = RandomChat.objects.all().exclude(user=self.user)
        try:
            return random.choice(peopleList)
        except IndexError:
            return None

    def removeRandomChat(self):
        return RandomChat.objects.get(user=self.user).delete()