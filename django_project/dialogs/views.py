from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    ListView,
    CreateView,
)
from .models import Message, Chat
from django.contrib.auth.models import User
from django.views.generic import View


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

    def get(self, request, id):
        users = User.objects.all()
        has_mess = False
        chat = Chat.objects.get(id=id)
        if chat.messages.count() != 0:
            has_mess = True
        return render(request, self.template, context={'users': users, 'chat': chat, 'has_mess': has_mess})





# class MessageCreate(LoginRequiredMixin, View):
#     model_form = MessageForm
#     template = 'mymessages/message_form.html'
#     raise_exception = True
#
#     def get(self, request):
#         form = self.model_form()
#         return render(request, self.template, context={'form': form})
#
#     def post(self, request):
#         bound_form = self.model_form(request.POST)
#
#         if bound_form.is_valid():
#             bound_form.instance.sender = self.request.user
#             bound_form.instance.chat.members.add(self.request.user)
#             bound_form.save()
#             id = bound_form.instance.chat.id
#             return redirect('chat_detail', id)
#         return redirect(request, self.template, context={'form': bound_form})



