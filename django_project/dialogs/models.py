from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image


class Chat(models.Model):
    members = models.ManyToManyField(User)
    chat_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_pics', blank=True)
    type = models.CharField(max_length=1, default='')

    def __str__(self):
        return f'Chatname: {self.chat_name}; members: {self.members.all()}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Message(models.Model):
    content = models.TextField(max_length=1000)
    date_send = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message {self.content} from {self.sender} to {self.chat} with date {self.date_send}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date_send']