from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)				# First name
    last_name = models.CharField(max_length=30)					# Last name
    userid = models.CharField("user id", max_length=30)			# User ID
    pwd = models.CharField("password", max_length=30)			# Password
    sm = models.BooleanField("site manager", default=False)		# Site-manager field

class Report(models.Model):

class Attachment(models.Model):
	