from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns(
    '',
    url(r'^teams/$', views.team_list),
    url(r'^teams/(?P<pk>[0-9]+)/$', views.team_detail),
)
