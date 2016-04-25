from django.conf import settings
from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
	url(r'^register-social', views.register_social, name='register-social'),
	url(r'^associate-social', views.associate_social, name='associate-social'),
	url(r'^register', views.register, name='register'),
	url(r'^login', views.user_login, name='login'),
	url(r'^logout', views.user_logout, name='logout'),
	url(r'^new-site-manager', views.new_site_manager, name='new-site-manager'),
	url(r'^suspend-user', views.suspend_user, name='suspend-user'),
	url(r'^restore-user', views.restore_user, name='restore-user'),
	url(r'^create-group', views.create_group, name='create-group'),
	url(r'^add-user-to-group', views.add_user_to_group, name='add-user-to-group'),
        #url(r'^fda_login/(?P<username>.*)/(?P<password>.*)/$', views.fda_login, name='fda_login'),
        url(r'^fda_login', views.fda_login, name='fda_login'),  
)
