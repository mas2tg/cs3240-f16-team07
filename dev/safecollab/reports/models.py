from django.db import models
from django import forms
from django.core.files.storage import FileSystemStorage
from safecollab import settings
from users.models import User


class Report(models.Model):
	creator = models.ForeignKey(User, related_name='creator')			# User ID of user who submitted report
	encrypted = models.BooleanField(default=False)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300)
	path = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='attachments', default=None, null=True)

class ReportForm(forms.ModelForm):	
	class Meta:
		model = Report
		fields = (
			"name",
			"description",
			"path",
			"encrypted",
		)
