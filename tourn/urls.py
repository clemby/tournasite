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
    url(r'^teams/update/(?P<pk>\d+)/$',
        views.TeamUpdate.as_view(),
        name='team_update'),
    url(r'^teams/create/$', views.TeamCreate.as_view(), name='team_create'),
    url(r'^teams/mine/$',
        views.UserAdministeredTeamList.as_view(),
        name='user_administered_teams'),

    url(r'^tournaments/$',
        views.TournamentList.as_view(),
        name='tournament_list'),
    url(r'^tournaments/(?P<pk>\d+)/$',
        views.TournamentDetail.as_view(),
        name='tournament_detail'),

    url(r'^tournaments/(?P<tournament_pk>\d+)/signup/$',
        views.SignupMain.as_view(),
        name='tournament_signup_main'),
    url(r'^tournaments/(?P<tournament_pk>\d+)/signup-team/$',
        views.TeamSignup.as_view(),
        name='tournament_signup_own_team'),
    url(r'^tournaments/(?P<tournament_pk>\d+)/signup-player/$',
        views.PlayerSignup.as_view(),
        name='tournament_signup_player'),
)
