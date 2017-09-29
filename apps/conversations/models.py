from __future__ import unicode_literals
from django.db import models
from ..new_users.models import User

# Create your models here.
class Conversation(models.Model):
    user = models.ManyToManyField(User)

class MessageManager(models.Manager):
    def validator(self, postData):
        errors = []
        if len(postData['message']) < 1:
            errors.append('Please enter a message')
        return errors

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=None, related_name='messages')
    sender = models.ForeignKey(User)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()