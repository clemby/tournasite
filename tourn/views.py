import json

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django import forms

from .models import (
    Team,
    Tournament,
    TeamEntry,
    PlayerRandomTeamEntry,
    Match,
)

from .forms import (
    TeamForm,
    TeamEntryForm,
    PlayerEntryForm,
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
                'name': entry.team.short_name or entry.team.name,
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
                'winner_next':
                match.winner_next.id if match.winner_next else None,
                'loser_next':
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

        allow_signup = request.user.is_authenticated() and not \
            tournament.contains_player(request.user)

        return render(request, self.template_name, {
            'tournament': tournament,
            'matches': match_list,
            'teams': teams_list,
            'as_json': json.dumps(tournament_data),
            'allow_signup': allow_signup,
        })

    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, pk=pk)
        return self.render_response(request, tournament)


class TournIndex(TournamentDetail):
    template_name = 'tourn/tournament_detail.html'

    def get(self, request):
        tournament = Tournament.get_current_or_404()
        return self.render_response(request, tournament)


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


class TeamCreate(generic.View):
    template_name = 'tourn/team_create.html'

    @method_decorator(login_required)
    def get(self, request):
        form = TeamForm()
        return render(request, self.template_name, {
            'form': form,
        })

    @method_decorator(login_required)
    def post(self, request):
        form = TeamForm(request.POST)
        if form.is_valid():
            form.instance.creator = request.user
            form.save(commit=True)

        return redirect(reverse('tourn:team_list'))


class PlayerSignupMixin(object):
    def get_player_signup_form(self, player_pk, tournament_pk):
        form = PlayerEntryForm({
            'player': player_pk,
            'tournament': tournament_pk,
        })

        form.fields['player'].widget = forms.HiddenInput()
        form.fields['tournament'].widget = forms.HiddenInput()

        return form


class PlayerSignup(generic.View, PlayerSignupMixin):
    form_template = 'tourn/player_signup.html'
    success_template = 'tourn/message.html'
    error_template = 'tourn/message.html'

    @method_decorator(login_required)
    def get(self, request, tournament_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)
        form = self.get_player_signup_form(
            player_pk=request.user.pk,
            tournament=tournament_pk
        )

        return render(request, self.form_template, {
            'form': form,
            'tournament': tournament,
        })

    @method_decorator(login_required)
    def post(self, request, tournament_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)
        form = PlayerEntryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return render(request, self.success_template, {
                'message': 'Registration successful!',
                'title': 'Registration successful!',
                'tournament': tournament,
            })

        return render(request, self.form_template, {
            'form': form,
            'tournament': tournament,
        })


class TeamSignupMixin(object):
    def get_team_signup_form_or_none(self, player_pk, tournament_pk):
        administered_teams = Team.objects.filter(
            admins__pk__contains=player_pk
        )

        if not administered_teams.exists():
            return None

        form = TeamEntryForm({
            'players': (player_pk,),
            'tournament': tournament_pk,
        })
        form.fields['tournament'].widget = forms.HiddenInput()
        form.fields['team'].choices.queryset = administered_teams

        return form


class TeamSignup(generic.View, TeamSignupMixin):
    template_name = 'tourn/team_signup.html'
    success_template_name = 'tourn/message.html'

    @method_decorator(login_required)
    def get(self, request, tournament_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)
        form = self.get_team_signup_form_or_none(
            player=request.user,
            tournament=tournament
        )

        return render(request, self.template_name, {
            'form': form,
            'tournament': tournament,
        })

    @method_decorator(login_required)
    def post(self, request, tournament_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)
        form = TeamEntryForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'tournament': tournament,
            })

        return render(request, self.success_template_name, {
            'message': 'Team successfully registered!',
            'title': 'Registration successful',
            'tournament': tournament,
        })


class SignupMain(generic.View, TeamSignupMixin, PlayerSignupMixin):
    template_name = 'tourn/signup_main.html'
    error_template_name = 'tourn/message.html'

    @method_decorator(login_required)
    def get(self, request, tournament_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)

        already_entered = PlayerRandomTeamEntry.objects.filter(
            player_pk=request.user.pk,
            tournament=tournament
        ).exists() or TeamEntry.objects.filter(
            players__pk__contains=request.user.pk,
            tournament=tournament
        ).exists()

        if already_entered:
            return render(request, self.error_template_name, {
                'message': "You've already entered that tournament!",
                'title': "Registration failed",
                'tournament': tournament,
            })

        team_signup_form = self.get_team_signup_form_or_none(
            player_pk=request.user.pk,
            tournament_pk=tournament_pk
        )

        player_signup_form = self.get_player_signup_form(
            player_pk=request.user.pk,
            tournament_pk=tournament_pk
        )

        return render(request, self.template_name, {
            'tournament': tournament,
            'forms': {
                'enter_team': team_signup_form,
                'enter_player': player_signup_form,
            },
            'tournament': tournament,
        })
