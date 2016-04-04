from django import forms
from reports.models import Report

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
