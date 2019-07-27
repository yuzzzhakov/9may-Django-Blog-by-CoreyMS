from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Message, Dialog, UserDialogs
from .forms import MessageForm
from django.contrib.auth.models import User
from django.views.generic import View, CreateView
from .utils import delete_empty_dialogs, get_dialogs_and_friends_without_dialogs


class Dialogs(LoginRequiredMixin, View):
    def get(self, request):
        context = get_dialogs_and_friends_without_dialogs(self.request.user)
        return render(request, 'dialogs/dialogs.html', context=context)


class DialogView(LoginRequiredMixin, View):
    def get(self, request, id):
        me = self.request.user
        context = get_dialogs_and_friends_without_dialogs(me)

        dialog = UserDialogs.objects.get(user=me).dialogs.get(id=id)
        receiver = None

        for member in dialog.members.all():
            if member != me:
                receiver = member
                break
        if not receiver:
            receiver = me

        context.update({'dialog': dialog, 'receiver': receiver, 'MessageForm': MessageForm})

        return render(request, 'dialogs/dialogs.html', context=context)


class DialogCheck(LoginRequiredMixin, View):
    def get(self, request, id):
        me = self.request.user
        if UserDialogs.objects.get(user=me).dialogs.filter(members=User.objects.get(id=id)):
            dialogs = UserDialogs.objects.get(user=me).dialogs.filter(members=User.objects.get(id=id)).annotate(num_members=Count('members'))
            for dialog in dialogs:
                if dialog.num_members == 1:
                    return redirect('dialog-view', id=dialog.id)
        else:
            return redirect('dialog-create-view', id=id)


class DialogCreateView(LoginRequiredMixin, View):
    def get(self, request, id):
        context = get_dialogs_and_friends_without_dialogs(self.request.user)
        receiver = User.objects.get(id=id)
        context.update({'receiver': receiver, 'MessageForm': MessageForm})
        return render(request, 'dialogs/dialog_new.html', context=context)


class DialogCreate(LoginRequiredMixin, View):
    model_form = MessageForm
    raise_exception = True

    def post(self, request, id):
        me = self.request.user
        receiver = User.objects.get(id=id)
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            dialog = Dialog.objects.create(dialog_name='dialog_' + str(me.username) + '_' + str(receiver.username), type='D')
            dialog.members.add(me)
            dialog.members.add(receiver)
            UserDialogs.objects.get(user=me.id).dialogs.add(dialog)
            UserDialogs.objects.get(user=id).dialogs.add(dialog)

            bound_form.instance.sender = self.request.user
            bound_form.instance.dialog = dialog
            bound_form.save()
            dialog.last_message_send_date = timezone.now()
            dialog.save()

        return redirect('dialog-view', id=dialog.id)


class MessageCreate(LoginRequiredMixin, View):
    model_form = MessageForm
    raise_exception = True

    def post(self, request, id):
        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            bound_form.instance.sender = self.request.user
            bound_form.instance.dialog = Dialog.objects.get(id=id)
            bound_form.save()
            chat = Dialog.objects.get(id=id)
            chat.last_message_send_date = timezone.now()
            chat.save()
            return redirect('dialog-view', id=id)

