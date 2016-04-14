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
    url(r'^users/', include('users.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^inbox/', include('inbox.urls')),
    url(r'^index', views.index, name='index'),
    url(r'^home', views.home, name='home'),
    url(r'^groups', views.groups, name='groups'),
    url(r'^$', views.index, name='index'),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)