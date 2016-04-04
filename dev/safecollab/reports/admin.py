from django.contrib import admin
from reports.models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Update the registeration to include this customised interface
admin.site.register(Report, ReportAdmin)