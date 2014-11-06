from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^teams/$', views.team_list),
    url(r'^teams/(?P<pk>[0-9]+)/$', views.team_detail),
)


urlpatterns = format_suffix_patterns(urlpatterns)
