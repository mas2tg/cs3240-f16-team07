from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_report/$', views.add_report, name='add_report'),
                       )
