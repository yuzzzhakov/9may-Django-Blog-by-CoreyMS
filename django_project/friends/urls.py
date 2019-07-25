from django.urls import path
from .views import *
from . import views
from . import models

urlpatterns = [
    path('friends/', FriendsView.as_view(), name='friends'),
    path('make-friend/<int:id>/', MakeFriendView.as_view(), name='make-friend'),
]

