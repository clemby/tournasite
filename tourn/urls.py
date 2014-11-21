from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.TournIndex.as_view(), name='index'),

    url(r'^success/$', views.MessageView.as_view(), name='success'),
    url(r'^error/$', views.MessageView.as_view(), name='error'),

    url(r'^teams/$', views.TeamList.as_view(), name='team_list'),
    url(r'^teams/(?P<pk>\d+)/$',
        views.TeamDetail.as_view(),
        name='team_detail'),
    url(r'^teams/create/$', views.TeamCreate.as_view(), name='team_create'),

    url(r'^tournaments/$',
        views.TournamentList.as_view(),
        name='tournament_list'),
    url(r'^tournaments/(?P<pk>\d+)/$',
        views.TournamentDetail.as_view(),
        name='tournament_detail'),

    url(r'^signup/(?P<tournament_pk>\d+)/random/$',
        views.PlayerSignupRandomTeam.as_view(),
        name='tournament_signup_random_team'),
)
