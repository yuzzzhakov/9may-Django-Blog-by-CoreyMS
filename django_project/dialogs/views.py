
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .models import Message, Chat
from .forms import MessageForm
from django.contrib.auth.models import User
from django.views.generic import View, CreateView


class Dialogs(LoginRequiredMixin, View):
    model = Chat
    template = 'dialogs/dialogs.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template, context={'users': users})


class DialogCheck(LoginRequiredMixin, View):
    template = 'dialogs/dialogs.html'

    def get(self, request, id):
        dialogs_with_self_user = self.request.user.chat_set.filter(type='D')
        requested_chat = None
        exit_flag = False
        receiver = User.objects.get(id=id)

        for chat in dialogs_with_self_user:
            for member in chat.members.all():
                if member == receiver:
                    requested_chat = chat
                    exit_flag = True
                    break
            if exit_flag:
                break

        if requested_chat is None:
            chat = Chat(chat_name='chat_'+str(self.request.user.username)+'_'+str(receiver.username), type='D')
            chat.save()
            chat.members.add(self.request.user)
            chat.members.add(receiver)
            return redirect('dialog-view', id=chat.id)
        else:
            return redirect('dialog-view', id=requested_chat.id)


class DialogView(LoginRequiredMixin, View):
    template = 'dialogs/dialogs.html'
    model_form = MessageForm

    def get(self, request, id):
        users = User.objects.all()
        has_mess = False
        chat = Chat.objects.get(id=id)

        members = chat.members.all()

        for user in members:
            if user != self.request.user:
                receiver = user
            else:
                receiver = self.request.user

        if chat.messages.count() != 0:
            has_mess = True
        return render(request, self.template, context={'users': users, 'chat': chat, 'receiver': receiver, 'has_mess': has_mess, 'form': self.model_form})


class MessageCreate(LoginRequiredMixin, View):
    model_form = MessageForm
    raise_exception = True

    def post(self, request, id):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            bound_form.instance.sender = self.request.user
            bound_form.instance.chat = Chat.objects.get(id=id)
            bound_form.save()
            # chat = bound_form.instance.chat
            return redirect('dialog-view', id=id)




