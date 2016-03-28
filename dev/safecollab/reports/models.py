from django.db import models

class Report(models.Model):
	user_id = models.CharField(max_length=30)			# User ID of user who submitted report
	encrypted = models.BooleanField(default=False)

class Attachment(models.Model):
	report_id = models.IntegerField()
	url = models.CharField(max_length=100)
