from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
	url(r'^add-report', views.add_report, name='add-report'),
	url(r'^add_folder', views.add_folder, name='add_folder'),
    url(r'^detail/(?P<file_name>.*)/$', views.detail, name='detail'),
    url(r'^edit/(?P<file_name>.*)/$', views.edit, name='edit'), #TODO: include report name in link
    url(r'^delete/(?P<file_name>.*)/$$', views.delete, name='delete'), #TODO: include report name in link
    url(r'^delete_file/(?P<path>.*)/(?P<report_name>.*)/$$', views.delete_file, name='delete_file'),
    url(r'^delete_folder/(?P<folder_id>.*)/$', views.delete_folder, name='delete_folder'),
    url(r'^(?P<folder_name>.*)/$$', views.index, name='reports'),
    url(r'^$', views.index, name='index'),

)
