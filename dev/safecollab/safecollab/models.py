from django.db import models

# Django automatically creates a primary_key field called 'id' if no primary_key is specified.
# id = models.IntegerField(primary_key=True)

class User(models.Model):
    first_name = models.CharField(max_length=30)		# First name
    last_name = models.CharField(max_length=30)			# Last name
    user_id = models.CharField(max_length=30)			# User ID
    password = models.CharField(max_length=30)			# Password
    site_manager = models.BooleanField(default=False)	# Site-manager field

class Report(models.Model):
	user_id = models.CharField(max_length=30)			# User ID of user who submitted report
	encrypted = models.BooleanField(default=False)

class Attachment(models.Model):
	report_id = models.IntegerField()
	url = models.CharField(max_length=100)
