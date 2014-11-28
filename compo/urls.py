from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'compo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.Home.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^tourn/', include('tourn.urls', namespace='tourn')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
