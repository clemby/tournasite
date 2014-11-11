from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from tourn.models import Team, Match, Tournament


class UserSerializer(serializers.ModelSerializer):
    teams = serializers.PrimaryKeyRelatedField(many=True)
    created_teams = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('username', 'id')


class UsernameSerializer(serializers.RelatedField):
    """Serializes User instances as their username."""
    read_only = False

    def to_native(self, user):
        return user.username

    def from_native(self, data):
        return get_object_or_404(User, username=data)


class CurrentMembersField(serializers.Field):
    read_only = True

    def field_to_native(self, obj, field_name):
        queryset = obj.get_current_members()
        if not queryset:
            return []
        return [tup[0] for tup in queryset.values_list('username')]


class TeamSerializer(serializers.ModelSerializer):
    """Serialize a team, with entries intact."""
    class Meta:
        model = Team
        fields = ('name', 'id', 'creator', 'entries', 'current_members')

    creator = serializers.Field(source='creator.username')
    current_members = CurrentMembersField()


class TeamNameSerializer(serializers.RelatedField):
    """Serializes Team instances as their name."""
    read_only = False

    def to_native(self, team):
        return team.name

    def from_native(self, data):
        return get_object_or_404(Team, name=data)


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('name', 'id', 'teams',)

    name = serializers.CharField(max_length=40, required=False)


class MatchNameSerializer(serializers.RelatedField):
    read_only = True

    def to_native(self, match):
        return match.name


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'id', 'min_team_size', 'max_team_size',
                  'min_teams_per_match', 'max_teams_per_match', 'matches')

    min_team_size = serializers.IntegerField(default=2, min_value=1)
    max_team_size = serializers.IntegerField(default=2, min_value=1)

    min_teams_per_match = serializers.IntegerField(default=2, min_value=1)
    max_teams_per_match = serializers.IntegerField(default=2, min_value=1)
