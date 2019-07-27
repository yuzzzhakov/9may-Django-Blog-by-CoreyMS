from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserFriends
from django.contrib.auth.models import User
from .utils import *


class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        me = self.request.user
        other_users = list(User.objects.all())
        friends = UserFriends.objects.get(user=me).friends.all()
        income_friend_requests = UserFriends.objects.get(user=me).income_friend_requests.all()
        outcome_friend_requests = UserFriends.objects.get(user=me).outcome_friend_requests.all()

        for user in friends:
            other_users.remove(user)
        for user in income_friend_requests:
            other_users.remove(user)
        for user in outcome_friend_requests:
            other_users.remove(user)

        return render(request, 'friends/friends.html', context={
            'friends': friends,
            'income_friend_requests': income_friend_requests,
            'outcome_friend_requests': outcome_friend_requests,
            'other_users': other_users,
        })


class AddToFriends(LoginRequiredMixin, View):
    def get(self, request, id):
        me = self.request.user
        my_future_friend = User.objects.get(id=id)

        my_UserFriends_note = UserFriends.objects.get(user=me)
        my_UserFriends_note.outcome_friend_requests.add(my_future_friend)

        ff_UserFriends_note = UserFriends.objects.get(user=my_future_friend)
        ff_UserFriends_note.income_friend_requests.add(me)

        # if src == 'profile':
        #     return redirect('profile', id=id)
        # if src == 'friends':
        #     return redirect('friends', id=id)

        return redirect('profile', id=id)


class ApplyToFriends(LoginRequiredMixin, View):
    def get(self, request, id):
        me = self.request.user
        my_future_friend = User.objects.get(id=id)

        my_UserFriends_note = UserFriends.objects.get(user=me)
        my_UserFriends_note.income_friend_requests.remove(my_future_friend)
        my_UserFriends_note.friends.add(my_future_friend)

        ff_UserFriends_note = UserFriends.objects.get(user=my_future_friend)
        ff_UserFriends_note.outcome_friend_requests.remove(me)
        ff_UserFriends_note.friends.add(me)

        return redirect('profile', id=id)


class DeleteFromFriends(LoginRequiredMixin, View):
    def get(self, request, id):
        me = self.request.user
        my_future_nofriend = User.objects.get(id=id)

        my_UserFriends_note = UserFriends.objects.get(user=me)
        my_UserFriends_note.income_friend_requests.add(my_future_nofriend)
        my_UserFriends_note.friends.remove(my_future_nofriend)

        fnf_UserFriends_note = UserFriends.objects.get(user=my_future_nofriend)
        fnf_UserFriends_note.outcome_friend_requests.add(me)
        fnf_UserFriends_note.friends.remove(me)

        return redirect('profile', id=id)