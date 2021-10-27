from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('signup/',views.signupView, name='signup'),
    path('profile/',views.profileView, name='profile'),
]
