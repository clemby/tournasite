from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.EventTimeline.as_view(), name='timeline'),
    url(r'^(?P<pk>\d+)/$', views.EventDetail.as_view(),
        name='event_detail'),
)
