from django.db import models
from django import forms
from django.core.files.storage import FileSystemStorage
from safecollab import settings
from users.models import User


class Report(models.Model):
	creator = models.ForeignKey(User, related_name='creator')			# User ID of user who submitted report
	encrypted = models.BooleanField(default=False)
	path = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='attachments', default=None, null=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300)

class ReportForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name.")
    description = forms.CharField(max_length=300, help_text="Please enter the description.")
    path = forms.FileField(help_text="Please select the report to upload")
    
    class Meta:
            model = Report
            fields = [
                "name",
                "description",
                "path"
            ]
