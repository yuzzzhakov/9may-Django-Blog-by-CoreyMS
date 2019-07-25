from django.db import models
from django.contrib.auth.models import User


class Friends(models.Model):
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend2')
    status1 = models.CharField(max_length=1, default='S')
    status2 = models.CharField(max_length=1, default='W')
