from django.db import models
from users.models import User



class Report(models.Model):
	creator = models.ForeignKey(User, default=None, null=True)			# User ID of user who submitted report
	encrypted = models.BooleanField(default=False)
	path = models.FileField()
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300)
class Attachment(models.Model):
	report_id = models.ForeignKey(Report)
	url = models.CharField(max_length=100)
