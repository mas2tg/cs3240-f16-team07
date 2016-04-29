from django.contrib import admin
from reports.models import Report, Folder, File

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Update the registeration to include this customised interface
admin.site.register(Report, ReportAdmin)

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Update the registeration to include this customised interface
admin.site.register(Folder, FolderAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ('path','report')

admin.site.register(File, FileAdmin)


#
# class FolderAdmin(admin.ModelAdmin):
#     list_display = ('name',)


# Update the registeration to include this customised interface
# admin.site.register(Folder, ReportAdmin)
