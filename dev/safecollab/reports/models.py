from django.db import models
from django import forms
from django.core.files.storage import FileSystemStorage
from safecollab import settings
from users.models import User

from datetime import datetime


class Folder(models.Model):
     creator = models.ForeignKey(User, related_name='folder_creator')
     # group_creator = models.ForeignKey(Gro)TODO:implement Group
     name = models.CharField(max_length=30)


class Report(models.Model):
    creator = models.ForeignKey(User, related_name='creator')  # User ID of user who submitted report
    encrypted = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=50)
    longDescription = models.CharField(max_length=1000, default='')
    private = models.BooleanField(default=False)
    time = models.DateTimeField(default=datetime.now)
    path = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to='attachments',
                            default=None, null=True)
    folder = models.ForeignKey(Folder, related_name='folder',null=True)





class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = (
            "name",
            "description",
            "longDescription",
            "path",
            "encrypted",
            "private",

        )
