from django import forms
from .models import *


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields =['content']

        widgets ={'content': forms.Textarea(attrs={'class': 'form-control'})}
