from django.contrib import admin
from reports.models import Report, Folder

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Update the registeration to include this customised interface
admin.site.register(Report, ReportAdmin)

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Update the registeration to include this customised interface
admin.site.register(Folder, FolderAdmin)


#
# class FolderAdmin(admin.ModelAdmin):
#     list_display = ('name',)


# Update the registeration to include this customised interface
# admin.site.register(Folder, ReportAdmin)
