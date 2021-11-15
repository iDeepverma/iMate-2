import json,random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.exceptions import DenyConnection
from . import models
from accounts.models import UserProfile,RandomFrnd

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

        # onlineStatus = await database_sync_to_async(self.getOnline)()

        # await self.send(text_data=json.dumps({
        #         'type':'status_update',
        #         'value':onlineStatus
        # }))

        return await super().receive(text_data=text_data, bytes_data=bytes_data)
    
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'sender':event['sender'],
                'receiver':event['receiver']
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
    
    # def getOnline(self):
    #     onlineStatus=UserProfile.objects.get(user=self.friend).isOnline
    #     return onlineStatus


class RandomChatPairer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated == False:
            raise DenyConnection('User not logged in')
        await database_sync_to_async(self.addRandomChat)()
        await self.channel_layer.group_add(                                    #adding channel layer to above two groups
            'randomChatPairingData',
            self.channel_name
        )
        return await self.accept()
    
    async def disconnect(self, code):
        await database_sync_to_async(self.removeRandomChat)()
        await self.channel_layer.group_discard(                                #removes channel name from above two groups
           'randomChatPairingData',
            self.channel_name
        )
        return await super().disconnect(code)
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        if message=='search':
            pairUser = await database_sync_to_async(self.getPair)()
            if pairUser == None:
                await self.send(text_data=json.dumps({
                    'type':'infoMsg',
                    'pairStatus':False
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type':'infoMsg',
                    'pairStatus':True,
                }))
                await self.channel_layer.group_send(
                    'randomChatPairingData',
                    {
                        'type':'pairing_data',
                        'forUser':pairUser.user.username
                    }
                )
        return await super().receive(text_data=text_data, bytes_data=bytes_data)

    async def pairing_data(self,event):
        if event['forUser'] == self.user.username:
            await self.send(text_data=json.dumps({
                'type':'infoMsg',
                'pairStatus':True,
            }))

    def addRandomChat(self):
        profile= self.user.profile
        profile.isRandom = True
        profile.save()

    def getPair(self):
        profile = self.user.profile
        peopleList = UserProfile.objects.filter(isRandom=True).exclude(user=self.user)
        try:
            pairUser=random.choice(peopleList)
            chatId = models.conversastionhash(pairUser.user,self.user)
            pairUser.randomChatId=chatId
            profile.randomChatId=chatId
            pairUser.save()
            profile.save()
            return pairUser
        except IndexError:
            return None

    def removeRandomChat(self):
        profile = self.user.profile
        profile.isRandom = False
        profile.save()
    

class RandomChat(AsyncWebsocketConsumer):
    
    async def connect(self):
        #Run when client connect to server via a websoclet
        self.user = self.scope['user']
        if self.user.is_authenticated == False:
            raise DenyConnection('User not logged in')
        
        self.groupName = await database_sync_to_async(self.getGroupName)()     #derives groupname for the user
        
        await database_sync_to_async(self.setOnline)(True)                     #sets its online status to true
        
        self.frndModel = await database_sync_to_async(self.setFrndModel)()

        await self.channel_layer.group_add(                                    #adding channel layer to above two groups
            self.groupName,
            self.channel_name
        )
        return await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_send(
            self.groupName,
            {
                'type': 'end_chat'
            }
        )                               
        await self.channel_layer.group_discard(                                #removes channel name from above two groups
            self.groupName,
            self.channel_name
        )
        await database_sync_to_async(self.setOnline)(False)                    #sets online status to false in profile database
        await database_sync_to_async(self.removeFrndModel)()
        return await super().disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        '''
            Gets events from the clients via the websocket.
            the type field in the text_data chooses which handler to run for that specific event
        '''

        data_obj = json.loads(text_data)
        if 'message' in data_obj:
            message = data_obj['message']                                          #raw message from the websocket
            await self.channel_layer.group_send(
                self.groupName,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender':self.user.username
                }
            )
        elif 'signal' in data_obj:
            if data_obj['signal'] == 'add_friend':
                await database_sync_to_async(self.addFriend)()

        return await super().receive(text_data=text_data, bytes_data=bytes_data)
    
    async def chat_message(self, event):
        message = event['message']
        if event['sender'] == self.user.username:
            sender='me'
        else:
            sender='notme'
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
                'sender': sender
        }))
    
    async def end_chat(self,event):
        await self.send(text_data=json.dumps({
                'type':'end_chat'
        }))


    def getGroupName(self):
        self.profile = self.user.profile
        return self.profile.randomChatId
    
    def setOnline(self, value):
        profile = UserProfile.objects.get(user=self.user)
        profile.isOnline = value
        profile.save()

    def setFrndModel(self):
        users = UserProfile.objects.filter(randomChatId=self.groupName).order_by('user')
        return RandomFrnd.objects.get_or_create(user1=users[0],user2=users[1])[0]
    
    def removeFrndModel(self):
        users = UserProfile.objects.filter(randomChatId=self.groupName).order_by('user')
        try:
            RandomFrnd.objects.get(user1=users[0],user2=users[1]).delete()
        except RandomFrnd.DoesNotExist:
            return None
    
    def addFriend(self):
        print('hello')
        frndModel = self.frndModel
        if frndModel.user1 == self.profile:
            print('one')
            frndModel.user1consent = True
            frndModel.save()
        elif self.frndModel.user2 == self.profile:
            print('two')
            frndModel.user2consent = True
            frndModel.save()
        
        if frndModel.user1consent ==True and self.frndModel.user2consent==True:
            print('done')
            frndModel.user1.userFriends.add(frndModel.user2.user)
            frndModel.user2.userFriends.add(frndModel.user1.user)
