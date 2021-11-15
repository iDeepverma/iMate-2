from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
      # path('login/', views.loginView, name='login'),
      path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
      path('logout/', views.logoutView, name='logout'),
      path('signup/', views.signupView, name='signup'),
      path('profile/', views.profileView, name='profile'),
      # path('search/<slug:username>/',views.searchView, name='search'),
]
