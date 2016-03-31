from django.conf.urls import patterns, include, url
from django.contrib import admin
from safecollab import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'safecollab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^home/', views.home, name='home'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^create-group/', views.create_group, name='create-group'),
    url(r'^group-summary', views.group_summary, name='group-summary'),
    url(r'^add-user-to-group', views.add_user_to_group, name='add-user-to-group'),
    url(r'^new-site-manager', views.new_site_manager, name='new-site-manager'),
    url(r'^suspend-user', views.suspend_user, name='suspend-user'),
    url(r'^restore-user', views.restore_user, name='restore-user'),
    url(r'^$', views.index, name='index'),
)
