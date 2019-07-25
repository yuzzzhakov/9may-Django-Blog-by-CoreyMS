from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Friends
from django.contrib.auth.models import User
from .utils import my_friends, income_friend_requests


class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        friends = my_friends(self.request.user.id)
        f_requests = income_friend_requests(self.request.user.id)

        return render(request, 'friends/friends.html', context={'friends': friends, 'f_requests': f_requests})


class MakeFriendView(LoginRequiredMixin, View):
    def get(self, request, id):
        Friends.objects.create(status1='S', status2='W', friend1=self.request.user, friend2=User.objects.get(id=id))
        return redirect('profile', id=id)

