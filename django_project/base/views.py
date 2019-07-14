from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render


def about(request):
    return render(request, 'base/about.html', {'title': 'About'})


class UsersListView(ListView):
    model = User
    template_name = 'base/all_users.html'
    context_object_name = 'users'

    def get_queryset(self):
        all_users = User.objects.all()
        return all_users


