from django import forms
from django.contrib.auth.models import User

from .models import (
    Team,
    TeamEntry,
    Match,
    PlayerRandomTeamEntry,
)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'admins')


class EntryFormBase(forms.ModelForm):
    def get_player_team_entry_error(self, players, tournament):
        entries = tournament.entries.filter(players__in=players)

        if not entries.exists():
            return None

        return 'Players have already entered: {}'.format(
            list(entries.values_list('players__username'))
        )

    def get_player_lone_entry_error(self, players, tournament):
        entries = tournament.player_entries.filter(player__in=players)

        if not entries.exists():
            return None

        return 'Players have already signed up (without team): {}'.format(
            list(entries.values_list('players__username'))
        )

    def get_player_errors(self, players, tournament):
        return filter(None, [
            self.get_player_team_entry_error(players, tournament),
            self.get_player_lone_entry_error(players, tournament),
        ])


class TeamEntryForm(EntryFormBase):
    players = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                             required=False)

    class Meta:
        model = TeamEntry
        fields = ('team', 'tournament', 'players')

    def clean(self):
        """Checks the team and players haven't already signed up."""
        cleaned_data = super(TeamEntryForm, self).clean()

        team = cleaned_data.get('team')
        tournament = cleaned_data.get('tournament')
        players = cleaned_data.get('players')

        if not tournament:
            return self.cleaned_data

        if team and team.has_entered(tournament):
            self.add_error(
                'team',
                'Team {} has already entered {}'.format(
                    team.name,
                    tournament.name or 'tournament'
                )
            )

        if players:
            player_errors = self.get_player_errors(
                players=players, tournament=tournament)

            if player_errors:
                self.add_error('players', player_errors)

        return self.cleaned_data


class PlayerEntryForm(EntryFormBase):
    class Meta:
        model = PlayerRandomTeamEntry
        fields = ('player', 'tournament')

    def clean(self):
        """Checks the player hasn't already entered."""
        cleaned_data = super(PlayerEntryForm, self).clean()

        player = cleaned_data.get('player')
        tournament = cleaned_data.get('tournament')

        if player and tournament:
            player_errors = self.get_player_errors(
                players=(player,),
                tournament=tournament
            )

            if player_errors:
                self.add_error('player', player_errors)

        return self.cleaned_data


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ()

    def clean(self):
        """Checks all teams are entered in the tournament."""
        teams = self.cleaned_data.get('teams')
        tournament = self.cleaned_data.get('tournament')

        if teams and tournament:
            missing_teams = [
                team.name for team in teams if not team.has_entered(tournament)
            ]
            if missing_teams:
                self.add_error('teams', [
                    "{} hasn't entered the tournament".format(name)
                    for name in missing_teams
                ])

        winner_next = self.cleaned_data.get('winner_next')
        if winner_next and tournament and \
                winner_next.tournament != tournament:
            self.add_error('winner_next',
                           'winner_next is not in this tournament')

        loser_next = self.cleaned_data.get('loser_next')
        if loser_next and tournament and \
                loser_next.tournament != tournament:
            self.add_error('loser_next',
                           'loser_next is not in this tournament')

        return self.cleaned_data
