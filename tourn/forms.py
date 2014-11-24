from django.core.exceptions import ValidationError
from django import forms

from .models import (
    Team,
    Match,
)


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'admins')


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match

    def clean(self):
        """Checks all teams are entered in the tournament."""
        teams = self.cleaned_data.get('teams')
        tournament = self.cleaned_data.get('tournament')

        if teams and tournament:
            missing_teams = [
                team.name for team in teams if not team.has_entered(tournament)
            ]
            if missing_teams:
                raise ValidationError({
                    'teams': [
                        "{} hasn't entered the tournament".format(name)
                        for name in missing_teams
                    ]
                })

        return self.cleaned_data
