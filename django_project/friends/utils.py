from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Friends
from django.contrib.auth.models import User


def my_friends(id):
    friends = []
    friends_notes = Friends.objects.filter(Q(Q(friend1=User.objects.get(id=id)) | Q(friend2=User.objects.get(id=id))) & Q(status1='F') & Q(status2='F'))
    for note in friends_notes:
        if note.friend1 != User.objects.get(id=id):
            friends.append(note.friend1)
        if note.friend2 != User.objects.get(id=id):
            friends.append(note.friend2)

    return friends


def income_friend_requests(id):
    f_requests = []
    f_request_notes = Friends.objects.filter(Q(friend2=User.objects.get(id=id)) & Q(status1='S') & Q(status2='W'))
    for note in f_request_notes:
        f_requests.append(note.friend1)

    return f_requests


def outcome_friend_requests(id):
    f_requests = []
    f_request_notes = Friends.objects.filter(Q(friend1=User.objects.get(id=id)) & Q(status1='S') & Q(status2='W'))
    for note in f_request_notes:
        f_requests.append(note.friend2)

    return f_requests
