from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


#     friends_notes = Friends.objects.filter(Q(Q(friend1=User.objects.get(id=id)) | Q(friend2=User.objects.get(id=id))) & Q(status1='F') & Q(status2='F'))


