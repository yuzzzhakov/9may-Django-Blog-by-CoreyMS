from django.db import models
from django.contrib.auth.models import User


class UserFriends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')
    income_friend_requests = models.ManyToManyField(User, related_name='income_friend_requests')
    outcome_friend_requests = models.ManyToManyField(User, related_name='outcome_friend_requests')
