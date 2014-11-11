from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import permissions, viewsets

from tourn.models import (
    Team,
    Match,
    Tournament,
)
from tourn.serializers import (
    TeamSerializer,
    UserSerializer,
    MatchSerializer,
    TournamentSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.creator = self.request.user


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    # Players will be users with at least one team.
    queryset = User.objects.annotate(
        num_entries=Count('tournament_entries')
    ).filter(num_entries__gt=0)

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
