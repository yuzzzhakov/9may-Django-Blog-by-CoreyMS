from django.contrib import admin
from .models import Message, Dialog, UserDialogs


admin.site.register(Message)
admin.site.register(Dialog)
admin.site.register(UserDialogs)
