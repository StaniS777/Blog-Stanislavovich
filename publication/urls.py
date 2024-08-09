from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from publication.views import (
        AddDislike,
        AddLike,
        PublicCreateView,
        PublicDetailView, 
        PublicListView, 
        MyPublicListView
    )


urlpatterns = [
    path('<int:pk>', PublicDetailView.as_view(), name='public_detail'),
    path('public_list', PublicListView.as_view(), name='public_list'),
    path('<int:pk>/like/', csrf_exempt(AddLike.as_view()), name='like'),
    path('<int:pk>/dislike/', csrf_exempt(AddDislike.as_view()), name='dislike'),
    path('my_publics', MyPublicListView.as_view(), name='my_publics'),
    path('create', PublicCreateView.as_view(), name='create_public'),
]