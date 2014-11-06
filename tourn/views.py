from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from tourn.models import Team
from tourn.serializers import TeamSerializer


class JSONResponse(HttpResponse):
    """An HttpResponse which renders its content into JSON."""
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def team_list(request):
    """List all teams, or create a new one."""
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TeamSerializer(data=data)

        if not serializer.is_valid():
            return JSONResponse(serializer.errors, status=400)

        serializer.save()
        return JSONResponse(serializer.data, status=201)


@csrf_exempt
def team_detail(request, pk):
    """Retrieve, update or delete a team."""
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return JSONResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TeamSerializer(team, data=data)

        if not serializer.is_valid():
            return JSONResponse(serializer.errors, status=400)

        serializer.save()
        return JSONResponse(serializer.data)

    if request.method == 'DELETE':
        team.delete()
        return HttpResponse(status=204)
