from django.contrib import admin
from django.urls import path, include

from user.views import (
    LoginView, 
    RegisterView, 
    logoutView,
    profile,
    update_profile, 
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logoutView.as_view(), name='logout'),
    path('profile', profile, name='profile'),
    path('edit_profile', update_profile, name='edit_profile'),
]