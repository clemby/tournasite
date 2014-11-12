from django.views import generic

from .models import Team, Tournament


class TournamentDetail(generic.DetailView):
    model = Tournament
    template_name = 'tourn/tournament_detail.html'
    context_object_name = 'tournament'


class TournamentList(generic.ListView):
    model = Tournament
    template_name = 'tourn/tournament_list.html'
    context_object_name = 'tournament_list'


class TeamDetail(generic.DetailView):
    model = Team
    template_name = 'tourn/team_detail.html'
    context_object_name = 'team'


class TeamList(generic.ListView):
    model = Team
    template_name = 'tourn/team_list.html'
    context_object_name = 'team_list'
