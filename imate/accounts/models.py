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
    randomAlias = models.CharField(max_length=20, blank = True, default = 'Anonymous')
    userHash = models.CharField(max_length=64, editable=False) #is also used as group name for channels
    randomPic = models.ImageField(null= True, blank=True, default = 'profilePics/anonymous.jpg' )   #user.randomPic = list[random_index]

    def save(self, *args, **kwargs):
        self.userHash = hashlib.sha256(self.user.username.encode()).hexdigest()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.user.username} Profile.'
