from django.conf.urls import patterns, url
from inbox import views

urlpatterns = patterns('',
	url(r'send', views.send, name='send'),
	url(r'^$', views.index, name='index'),
)
