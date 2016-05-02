from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from safecollab import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'safecollab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^inbox/', include('inbox.urls', namespace='inbox')),
    url(r'^groups/', include(patterns('',
            url(r'^(?P<group_id>\d+)/', views.group_summary, name='group-summary'),
            url(r'^$', views.groups, name='groups'),
        ))),
    url(r'^home/', views.home, name='home'),
    url(r'^search/', views.search, name='search'),
    url(r'^$', views.index, name='index'),
    url(r'^fda_index/$', views.fda_index, name='fda_index'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
