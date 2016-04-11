from django.db import models
from django import forms
from users.models import User
from datetime import datetime
from django.utils.timezone import localtime

MAX_MESSAGE_LENGTH = 2000

class Message(models.Model):
	sender = models.ForeignKey(User, related_name='sender')				# User ID of user sent message
	recipient = models.ForeignKey(User, related_name='recipient')		# User ID of user that message was sent to
	body = models.CharField(max_length=MAX_MESSAGE_LENGTH)
	timestamp = models.DateTimeField(auto_now_add=True)
	read = models.BooleanField(default=False)
	encrypted = models.BooleanField(default=False)
	key = models.BinaryField(default=None, null=True)
	
	@property
	def sent_today(self):
		return datetime.today().date() == localtime(self.timestamp).date()