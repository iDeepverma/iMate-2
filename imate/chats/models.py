from django.db import models
from django.conf import settings
from hashlib import sha256
from django.contrib.auth import get_user_model

def conversastionhash(a, b):
    """
    :param a: User object
    :param b: User object
    :return: hexadecimal hash (length = 512)of usernames of both the user such that it is always unique
    for any two given users
    """
    user1 = a.username.encode()
    user2 = b.username.encode()
    hashstr = user1 + user2 if a.id < b.id else user2 + user1
    return sha256(hashstr).hexdigest()


# Create your models here.
class Message(models.Model):
    message = models.TextField()
    receiver = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="receiver")
    sender = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="sender")
    timestamp = models.DateTimeField(auto_now_add=True)
    userHash = models.CharField(max_length=64, editable=False, null=True)
    isRead = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.userHash = conversastionhash(self.receiver,self.sender)
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sender) + "@" + str(self.receiver)



class RandomChat(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='randomChatData'
    )
    chatId = models.CharField(null=True,blank=True,max_length=50)
    isPair = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.user.username
