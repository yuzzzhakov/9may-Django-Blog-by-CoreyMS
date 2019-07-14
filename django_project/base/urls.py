from . import views
from django.urls import include, path
from .views import UsersListView


urlpatterns = [
    path('about/', views.about, name='blog-about'),
    path('all-users/', UsersListView.as_view(), name='all-users'),
]