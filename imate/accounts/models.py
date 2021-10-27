from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True
    )
    userBio = models.CharField(
        max_length=150, 
        blank=True, 
        default='Hello World!'
    )
    userPic = models.ImageField(
        upload_to = 'userData/profilePic/',
        blank = True,
        null = True
    )
    isOnline = models.BooleanField(
        default=False,
        null=False
    )
    randomAlias = models.CharField(max_length=20, blank = True)
    userHash = models.CharField(max_length=64)
    randomPic = models.IntegerField(null= True)
    def __str__(self) -> str:
        return self.user.username
