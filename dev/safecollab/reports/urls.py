from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
	url(r'^add-report', views.add_report, name='add-report'),
)
