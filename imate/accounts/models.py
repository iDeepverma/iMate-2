import hashlib
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    userBio = models.CharField(
        max_length=150, 
        blank=True, 
        default='Hello World!'
    )
    userPic = models.ImageField(
        upload_to = 'profilePics/',
        default = 'profilePics/default.jpg',
        null = True
    )
    isOnline = models.BooleanField(
        default=False,
        null=False
    )
    userFriends = models.ManyToManyField(
        get_user_model(),
        related_name='friends',
        blank=True
    )
    randomAlias = models.CharField(max_length=30, blank = True, default = 'Anonymous')
    userHash = models.CharField(max_length=64, editable=False) #is also used as group name for channels
    randomPic = models.ImageField(null= True, blank=True, default = 'profilePics/anonymous.jpg' ) 
    isRandom = models.BooleanField(default=False)  #true when searching for random
    randomChatId = models.CharField(max_length=64,blank=True,null=True)
     
    def save(self, *args, **kwargs):
        self.userHash = hashlib.sha256(self.user.username.encode()).hexdigest()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.user.username


class RandomFrnd(models.Model):
    user1 = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='random_frnd'
    )
    user2 = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='random_self'
    )
    chatHash = models.CharField(max_length=64,blank=True,null=True)
    user1consent = models.BooleanField(default=False)
    user2consent = models.BooleanField(default=False)
