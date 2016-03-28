from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)		# First name
    last_name = models.CharField(max_length=30)			# Last name
    user_id = models.CharField(max_length=30)			# User ID
    password = models.CharField(max_length=30)			# Password
    site_manager = models.BooleanField(default=False)	# Site-manager field

