from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tourn.models import Team
from tourn.serializers import TeamSerializer


@api_view(['GET', 'POST'])
def team_list(request):
    """List all teams, or create a new one."""
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    """Retrieve, update or delete a team."""
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
