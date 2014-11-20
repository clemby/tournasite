import json

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render, get_object_or_404

from .models import (
    Team,
    Tournament,
    TeamEntry,
    PlayerRandomTeamEntry,
    Match,
)


class MessageView(generic.TemplateView):
    template_name = 'tourn/message.html'

    def get_context_data(self, title=None, message=None, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['message'] = message
        return context


class TournamentDetail(generic.View):
    template_name = 'tourn/tournament_detail.html'

    def get_team_list(self, tournament):
        entries = TeamEntry.objects.filter(tournament=tournament)
        return [
            {
                'name': entry.team.name,
                'id': entry.team.id,
                'members': list(entry.players.values('username', 'id')),
            }
            for entry in entries
        ]

    def get_match_list(self, tournament):
        matches = Match.objects.filter(tournament=tournament)
        return [
            {
                'id': match.id,
                'name': match.name,
                'teams': [team.id for team in match.teams.all()],
                'winner': match.winner.id if match.winner else None,
                'winnerNext':
                match.winner_next.id if match.winner_next else None,
                'loserNext':
                match.loser_next.id if match.loser_next else None,
            }
            for match in matches
        ]

    def render_response(self, request, tournament):
        teams_list = self.get_team_list(tournament)
        match_list = self.get_match_list(tournament)

        tournament_data = {
            'matches': match_list,
            'teams': teams_list,
        }

        return render(request, self.template_name, {
            'tournament': tournament,
            'matches': match_list,
            'teams': teams_list,
            'as_json': json.dumps(tournament_data),
        })

    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        return self.render_response(request, tournament)


class TournIndex(TournamentDetail):
    template_name = 'tourn/tournament_detail.html'

    def get(self, request):
        tournament = Tournament.get_current_or_404()
        return self.render_response(request, tournament)


class PlayerSignupRandomTeam(generic.View):
    success_template = 'tourn/message.html'
    error_template = 'tourn/message.html'

    @method_decorator(login_required)
    def get(self, request, tournament_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)

        already_entered = PlayerRandomTeamEntry.objects.filter(
            player=request.user,
            tournament=tournament_pk
        ).exists() or TeamEntry.objects.filter(
            players__contains=request.user,
            tournament=tournament_pk
        ).exists()

        if already_entered:
            return render(request, self.error_template, {
                'message': "You've already entered that tournament!",
                'title': "Registration failed",
            })

        entry = PlayerRandomTeamEntry(tournament=tournament,
                                      player=request.user)
        entry.save()

        return render(request, self.success_template, {
            'message': "Registration successful!",
            'title': 'Registration successful!',
        })


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
