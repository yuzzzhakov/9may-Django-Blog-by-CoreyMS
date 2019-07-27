from .models import Dialog, UserDialogs
from django.contrib.auth.models import User


def delete_empty_dialogs(me):
    if UserDialogs.objects.filter(user=me).first():
        user_dialogs = UserDialogs.objects.get(user=me).dialogs.all()
        for dialog in user_dialogs:
            if dialog.messages.all().count() == 0:
                dialog.delete()


def get_dialogs_and_friends_without_dialogs(me):
    delete_empty_dialogs(me)
    friends_without_chat = list(User.objects.all())
    user_dialog_list = UserDialogs.objects.filter(user=me).first().dialogs.all().order_by('-last_message_send_date')
    dialog_list = []

    for dialog in user_dialog_list:
        if dialog.members.count() == 1:
            dialog_list.append([dialog, me])
            friends_without_chat.remove(me)
        for member in dialog.members.all():
            if member != me:
                receiver = member
                dialog_list.append([dialog, receiver])
            if (member != me) and (member in friends_without_chat):
                friends_without_chat.remove(member)

    context = {'dialog_list': dialog_list, 'friends_without_chat': friends_without_chat}

    return context
