from django.conf.urls import patterns, url
from inbox import views

urlpatterns = patterns('',
	url(r'send', views.send, name='send'),
	url(r'delete', views.delete, name='delete'),
	url(r'mark-as-read', views.mark_as_read, name='mark-as-read'),
	url(r'mark-as-unread', views.mark_as_unread, name='mark-as-unread'),
	url(r'^$', views.index, name='index'),
)
