from django.conf import settings
from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
	url(r'^register-social', views.register_social, name='register-social'),
	url(r'^associate-social', views.associate_social, name='associate-social'),
	url(r'^register', views.register, name='register'),
	url(r'^login', views.user_login, name='login'),
	url(r'^logout', views.user_logout, name='logout'),
	url(r'^grant-sm/(?P<user_id>\d+)/', views.grant_sm, name='grant-sm'),
	url(r'^revoke-sm/(?P<user_id>\d+)/', views.revoke_sm, name='revoke-sm'),
	url(r'^suspend-user/(?P<user_id>\d+)/', views.suspend_user, name='suspend-user'),
	url(r'^restore-user/(?P<user_id>\d+)/', views.restore_user, name='restore-user'),
	url(r'^favorite-group', views.favorite_group, name='favorite-group'),
	url(r'^unfavorite-group', views.unfavorite_group, name='unfavorite-group'),
	url(r'^create-group', views.create_group, name='create-group'),
	url(r'^add-user-to-group', views.add_user_to_group, name='add-user-to-group'),
	url(r'^remove-user-from-group/(?P<group_id>\d+)/(?P<user_id>\d+)/', views.remove_user_from_group, name='remove-user-from-group'),
	url(r'^edit-profile', views.edit_profile, name='edit-profile'),
	url(r'^(?P<user_id>\d+)/(?P<editing>.*)/', views.view_profile, name='view-profile-editing'),
	url(r'^(?P<user_id>\d+)/', views.view_profile, name='view-profile'),

        url(r'^fda_login', views.fda_login, name='fda_login'),  
)
