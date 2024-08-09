from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from user.views import (
    LoginView, 
    RegisterView,
    follow_user,
    logoutView,
    profile,
    profile_detail,
    unfollow_user,
    update_profile, 
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logoutView.as_view(), name='logout'),
    path('me', profile, name='my_profile'),
    path('me/update', update_profile, name='my_profile_update'),
    path('<int:pk>', profile_detail, name='profile_detail'),
    path('edit_profile', update_profile, name='edit_profile'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),    
]