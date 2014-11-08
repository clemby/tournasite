from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'tournaments', views.TournamentViewSet)
