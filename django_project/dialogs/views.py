from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .models import Message, Chat
from .forms import MessageForm
from django.contrib.auth.models import User
from django.views.generic import View, CreateView


class Dialogs(LoginRequiredMixin, View):

    def get(self, request):
        chats = Chat.objects.filter(members=self.request.user)
        for chat in chats:
            if chat.messages.count() == 0:
                chat.delete()

        chats = Chat.objects.filter(members=self.request.user).order_by('-last_message_send_date')

        list = []
        receiver = None
        for chat in chats:
            for member in chat.members.all():
                if member != self.request.user:
                    receiver = member
                else: receiver = self.request.user
            list.append([chat, receiver])
        return render(request, 'dialogs/dialogs.html', context={'list': list})


class DialogView(LoginRequiredMixin, View):

    def get(self, request, id):

        chats = Chat.objects.filter(members=self.request.user)
        for chat in chats:
            if chat.messages.count() == 0:
                chat.delete()

        chats = Chat.objects.filter(members=self.request.user).order_by('-last_message_send_date')

        list = []
        receiver = None
        for chat in chats:
            for member in chat.members.all():
                if member != self.request.user:
                    receiver = member
                else: receiver = self.request.user

            list.append([chat, receiver])

        chat = Chat.objects.get(id=id)

        for member in chat.members.all():
            if member != self.request.user:
                receiver = member
                break

        return render(request, 'dialogs/dialogs.html', context={'list': list, 'chat': chat, 'receiver': receiver, 'form': MessageForm})


class MessageCreate(LoginRequiredMixin, View):
    model_form = MessageForm
    raise_exception = True

    def post(self, request, id):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            bound_form.instance.sender = self.request.user
            bound_form.instance.chat = Chat.objects.get(id=id)
            bound_form.save()
            chat = Chat.objects.get(id=id)
            chat.last_message_send_date = timezone.now()
            chat.save()
            # chat = bound_form.instance.chat
            return redirect('dialog-view', id=id)




