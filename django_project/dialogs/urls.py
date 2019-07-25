from django.urls import path
from .views import (
    Dialogs,
    DialogView,
    MessageCreate,
    DialogCreate,
)
from . import views

urlpatterns = [
    path('dialogs/', Dialogs.as_view(), name='dialogs'),
    path('dialogs/<int:id>/', DialogView.as_view(), name='dialog-view'),
    path('dialogs/message_create_<int:id>/', MessageCreate.as_view(), name='message-create'),
    path('dialog/chat_create_<int:id>/', DialogCreate.as_view(), name='dialog-create')
]

