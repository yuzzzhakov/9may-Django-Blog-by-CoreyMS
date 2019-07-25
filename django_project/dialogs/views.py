from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Message, Chat
from .forms import MessageForm
from django.contrib.auth.models import User
from django.views.generic import View, CreateView
from friends.utils import my_friends


class Dialogs(LoginRequiredMixin, View):

    def get(self, request):

        # making chat list

        chats = Chat.objects.filter(members=self.request.user)
        for chat in chats:
            if chat.messages.count() == 0:
                chat.delete()
        chats = Chat.objects.filter(members=self.request.user).order_by('-last_message_send_date')

        # making [chat, receiver] list and friends_without_chat

        list = []
        receiver = None
        friends_without_chat = my_friends(self.request.user.id)
        for chat in chats:
            for member in chat.members.all():
                if member != self.request.user:
                    receiver = member
                    if receiver in friends_without_chat:
                        friends_without_chat = friends_without_chat.remove(receiver)
                    break
                else:
                    receiver = self.request.user
            list.append([chat, receiver])

        return render(request, 'dialogs/dialogs.html', context={'list': list,
                                                                'friends_without_chat': friends_without_chat})


class DialogView(LoginRequiredMixin, View):

    def get(self, request, id):

        # making chat list

        chats = Chat.objects.filter(members=self.request.user)
        for chat in chats:
            if (chat.messages.count() == 0)and(chat != Chat.objects.get(id=id)):
                chat.delete()
        chats = Chat.objects.filter(members=self.request.user).order_by('-last_message_send_date')

        # making [chat, receiver] list and friends_without_chat

        list = []
        receiver = None
        friends_without_chat = my_friends(self.request.user.id)
        for chat in chats:
            for member in chat.members.all():
                if member != self.request.user:
                    receiver = member
                    if receiver in friends_without_chat:
                        friends_without_chat = friends_without_chat.remove(receiver)
                    break
                else:
                    receiver = self.request.user
            list.append([chat, receiver])

        # making receiver for chat

        chat = Chat.objects.get(id=id)
        receiver = None

        for member in chat.members.all():
            if member != self.request.user:
                receiver = member
                break

        if not receiver:
            receiver = self.request.user

        return render(request, 'dialogs/dialogs.html', context={'list': list,
                                                                'chat': chat,
                                                                'receiver': receiver,
                                                                'form': MessageForm,
                                                                'friends_without_chat': friends_without_chat})


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
            return redirect('dialog-view', id=id)


class DialogCreate(LoginRequiredMixin, View):

    def get(self, request, id):

        receiver = User.objects.get(id=id)
        sender = self.request.user
        new_chat = None

        if Chat.objects.filter(members=sender).filter(members=receiver).annotate(members_count=Count('members')).filter(members_count=1).first():
            new_chat = Chat.objects.filter(members=sender).filter(members=receiver).annotate(members_count=Count('members')).filter(members_count=1).first()
        else:
            new_chat = Chat.objects.create(chat_name='chat_'+str(sender.username)+str(receiver.username), type='D')
            new_chat.members.add(sender, receiver)

        return redirect('dialog-view', id=new_chat.id)




