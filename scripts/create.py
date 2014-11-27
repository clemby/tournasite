"""
Create a simple, single-elimination demo tournament with 8 teams.

"""
from django.contrib.auth.models import User

from .utils import generate_tournament


teams = ['Team {}'.format(i) for i in range(1, 9)]

team_defaults = {
    'creator': User.objects.get(pk=1),
}


generate_tournament(
    teams=teams,
    team_defaults=team_defaults
)
