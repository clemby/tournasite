from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from tourn.models import Team


class UserSerializer(serializers.ModelSerializer):
    teams = serializers.PrimaryKeyRelatedField(many=True)
    created_teams = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('username', 'id', 'teams')


class UsernameSerializer(serializers.RelatedField):
    """Serializes User objects as their username."""
    read_only = False

    def to_native(self, user):
        return user.username

    def from_native(self, data):
        return get_object_or_404(User, username=data)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'members', 'id', 'creator')

    creator = serializers.Field(source='creator.username')
    members = UsernameSerializer(many=True)
