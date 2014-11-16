from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^success/$', views.MessagePage.as_view(), name='success'),
    url(r'^error/$', views.MessagePage.as_view(), name='error'),

    url(r'^teams/$', views.TeamList.as_view(), name='team_list'),
    url(r'^teams/(?P<pk>\d+)/$',
        views.TeamDetail.as_view(),
        name='team_detail'),

    url(r'^tournaments/$',
        views.TournamentList.as_view(),
        name='tournament_list'),
    url(r'^tournaments/(?P<pk>\d+)/$',
        views.TournamentDetail.as_view(),
        name='tournament_detail'),
)
