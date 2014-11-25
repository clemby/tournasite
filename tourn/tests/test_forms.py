from django.contrib.auth.models import User

import mock

from .. import forms
from .. import models

from . import util as testutil


class TeamEntryFormTestCase(testutil.RequiresTeamEntriesTestCase):
    def setUp(self):
        self.form = forms.TeamEntryForm()
        self.setup_users()
        self.setup_tournament()

    def test_get_player_team_entry_errors_empty_if_users_not_entered(self):
        self.assertEqual(
            self.form.get_player_team_entry_errors(
                players=User.objects.all(),
                tournament=self.tournament
            ),
            []
        )

    def test_get_player_team_entry_errors_has_error_for_each_entered_player(
        self
    ):
        teams = [
            self.create_team(
                creator=self.users[2 * i],
                name='Team {}'.format(i)
            )
            for i in range(2)
        ]

        for i, team in enumerate(teams):
            self.create_team_entry(
                tournament=self.tournament,
                team=team,
                players=self.users[2 * i: 2 * (i + 1)]
            )

        errors = self.form.get_player_team_entry_errors(
            players=User.objects.all(),
            tournament=self.tournament
        )

        self.assertEqual(len(errors), 4)

        for i in range(4):
            self.assertIn(self.users[i].username, errors[i])
            self.assertIn('has already entered', errors[i])
            self.assertIn('team', errors[i])

    def test_get_player_lone_entry_errors_empty_if_users_not_entered(self):
        self.assertEqual(
            self.form.get_player_lone_entry_errors(
                players=User.objects.all(),
                tournament=self.tournament
            ),
            []
        )

    def test_get_player_lone_entry_errors_has_error_for_each_entered_player(
        self
    ):
        entries = []
        for i in range(3):
            entry = models.PlayerRandomTeamEntry(
                tournament=self.tournament,
                player=self.users[i]
            )
            entry.save()
            entries.append(entry)

        errors = self.form.get_player_lone_entry_errors(
            players=User.objects.all(),
            tournament=self.tournament
        )

        self.assertEqual(len(errors), len(entries))
        for i, err in enumerate(errors):
            self.assertIn(self.users[i].username, err)
            self.assertIn('entered alone', err)

    def test_clean_adds_team_error_if_team_has_entered(self):
        team = self.create_team(name='Test team', creator=self.users[0])
        self.create_team_entry(team=team, tournament=self.tournament)

        self.form = forms.TeamEntryForm({
            'players': (),
            'team': team.id,
            'tournament': self.tournament.id,
        })

        self.form.is_valid()

        team_errors = self.form.errors.get('team')

        self.assertNotEqual(team_errors, None)
        self.assertEqual(len(team_errors), 1)

        error = team_errors[0]
        self.assertIn(team.name, error)
        self.assertIn('has already entered', error)

    @mock.patch(
        'tourn.forms.TeamEntryForm.get_player_team_entry_errors',
        mock.Mock(side_effect=lambda *args, **kwargs: ['team_entry_errors'])
    )
    @mock.patch(
        'tourn.forms.TeamEntryForm.get_player_lone_entry_errors',
        mock.Mock(side_effect=lambda *args, **kwargs: ['lone_entry_errors'])
    )
    def test_clean_adds_player_errors_if_any(self):
        team = self.create_team(name='Test team', creator=self.users[0])
        self.create_team_entry(team=team, tournament=self.tournament)

        self.form = forms.TeamEntryForm({
            'players': (1,),
            'team': team.id,
            'tournament': self.tournament.id,
        })

        self.form.is_valid()

        self.assertEqual(
            self.form.errors.get('players'),
            ['team_entry_errors', 'lone_entry_errors']
        )
