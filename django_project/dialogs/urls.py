from django.urls import path
from .views import (
    Dialogs,
    DialogView,
    DialogCheck,
    MessageCreate,
)
from . import views

urlpatterns = [
    path('dialogs/', Dialogs.as_view(), name='dialogs'),
    path('dialogs/check_<int:id>/', DialogCheck.as_view(), name='dialog-check'),
    path('dialogs/<int:id>/', DialogView.as_view(), name='dialog-view'),
    path('dialogs/message_create_<int:id>/', MessageCreate.as_view(), name='message-create'),
]

