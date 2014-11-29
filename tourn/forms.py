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
    def get_player_team_entry_errors(self, players, tournament):
        entered_with_team = players.filter(
            tournament_entries__tournament=tournament
        )

        if not entered_with_team.exists():
            return []

        return [
            '{} has already entered with another team'.format(
                player.username
            )
            for player in entered_with_team
        ]

    def get_player_lone_entry_errors(self, players, tournament):
        entered_alone = players.filter(
            tournament_random_team_entries__tournament=tournament
        )

        if not entered_alone.exists():
            return []

        return [
            '{} has already entered alone'.format(
                player.username
            )
            for player in entered_alone
        ]


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
            player_errors = self.get_player_team_entry_errors(
                players=players,
                tournament=tournament
            ) + self.get_player_lone_entry_errors(
                players=players,
                tournament=tournament
            )

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
            errors = self.get_player_lone_entry_errors(
                players=(player,),
                tournament=tournament
            ) + self.get_player_team_entry_errors(
                players=(player,),
                tournament=tournament
            )

            if errors:
                self.add_error('player', errors)

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
