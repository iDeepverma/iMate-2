from django.contrib import admin
from .models import RandomFrnd, UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(RandomFrnd)