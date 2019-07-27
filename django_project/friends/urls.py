from django.urls import path
from .views import FriendsView, AddToFriends, ApplyToFriends, DeleteFromFriends
from . import views
from . import models

urlpatterns = [
    path('my-friends/', FriendsView.as_view(), name='my-friends'),
    path('add-to-friend/<int:id>/', AddToFriends.as_view(), name='add-to-friends'),
    path('apply-to-friends/<int:id>/', ApplyToFriends.as_view(), name='apply-to-friends'),
    path('delete-from-friends/<int:id>/', DeleteFromFriends.as_view(), name='delete-from-friends'),
]

