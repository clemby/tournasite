from rest_framework import serializers
from tourn.models import Team
from django.contrib.auth.models import User


class TeamSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(required=True, max_length=100)

    # TODO: players?

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new Team instance, given a dict of deserialized
        field values.

        Note: if we don't define this method, then deserializing data will
        simply return a dict of items.
        """
        if not instance:
            return Team(**attrs)

        instance.name = attrs.get('name', instance.name)

        players = attrs.get('players')
        if players:
            instance.players = User.objects.filter(username__in=players)
