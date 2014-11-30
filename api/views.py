from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import (
    viewsets,
)

from tourn.models import (
    Team,
    TeamEntry,
    Match,
    Tournament,
)
from tourn.serializers import (
    TeamSerializer,
    TeamEntrySerializer,
    UserSerializer,
    MatchSerializer,
    TournamentSerializer,
)

from . import permissions


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_fields = ('name', 'creator', 'admins', 'entries')

    def pre_save(self, obj):
        obj.creator = self.request.user


class TeamEntryViewSet(viewsets.ModelViewSet):
    queryset = TeamEntry.objects.all()
    serializer_class = TeamEntrySerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_fields = ('team', 'tournament', 'players')


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    # Players will be users with at least one team.
    queryset = User.objects.annotate(
        num_entries=Count('tournament_entries')
    ).filter(num_entries__gt=0)

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_fields = (
        'id',
        'username',
        'administered_teams',
        'created_teams',
    )
    search_fields = ('username',)


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_fields = ('tournament', 'winner', 'teams', 'name')
    search_fields = ('name',)


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_fields = (
        'name',
        'min_team_size',
        'max_team_size',
        'min_teams_per_match',
        'max_teams_per_match',
        'planned_start',
        'planned_finish'
    )
    search_fields = ('name',)
