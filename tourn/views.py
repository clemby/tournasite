from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import generics, permissions

from .models import Team
from .serializers import TeamSerializer, UserSerializer


class TeamBase:
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.creator = self.request.user


class TeamList(TeamBase, generics.ListCreateAPIView):
    pass


class TeamDetail(TeamBase, generics.RetrieveUpdateDestroyAPIView):
    pass


class PlayerBase:
    # Players will be users with at least one team.
    queryset = User.objects.annotate(
        num_teams=Count('teams')
    ).filter(num_teams__gt=0)

    serializer_class = UserSerializer


class PlayerList(PlayerBase, generics.ListCreateAPIView):
    pass


class PlayerDetail(PlayerBase, generics.RetrieveUpdateDestroyAPIView):
    pass
