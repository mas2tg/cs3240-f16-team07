from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
	url(r'^add-report', views.add_report, name='add-report'),
    url(r'^$', views.index, name='index'),
    # url(r'^attachments/(?P<link_to_file>.*)/$', views.download,name='download')
)
