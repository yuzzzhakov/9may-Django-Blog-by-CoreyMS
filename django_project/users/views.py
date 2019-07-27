from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.models import User

from dialogs.models import UserDialogs
from friends.models import UserFriends


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You are now able to log in')
            username = form.instance.username
            user = User.objects.get(username=username)
            UserDialogs.objects.create(user=user)
            UserFriends.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def options(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

        messages.success(request, f'Your account has been updated.')
        return redirect('options')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/options.html', context)


class ProfileView(View):
    def get(self, request, id):
        me = self.request.user
        viewed_user = User.objects.get(id=id)
        if viewed_user in UserFriends.objects.get(user=me).friends.all():
            friend_status = 'friend'
        elif viewed_user in UserFriends.objects.get(user=me).income_friend_requests.all():
            friend_status = 'request_to_friends'
        elif viewed_user in UserFriends.objects.get(user=me).outcome_friend_requests.all():
            friend_status = 'you_sent_request'
        else:
            friend_status = 'not_friend'
        return render(request, 'users/profile.html', context={'viewed_user': viewed_user, 'friend_status': friend_status})








