from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from . import models


class RequiresUsersTestCase(TestCase):
    def setup_users(self):
        self.users = [
            User(username='Test user {}'.format(i))
            for i in [1, 2, 3, 4, 5, 6, 7, 8]
        ]
        for user in self.users:
            user.save()


class RequiresTournamentTestCase(TestCase):
    def setup_tournament(self, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'test tournament'

        if 'planned_start' not in kwargs:
            kwargs['planned_start'] = timezone.now()

        self.tournament = models.Tournament(**kwargs)
        self.tournament.save()


class RequiresTeamsTestCase(TestCase):
    def setup_teams(self):
        user_range = range(len(self.users) / 2)

        self.teams = [
            models.Team(name='Team {}'.format(i), creator=self.users[2 * i])
            for i in user_range
        ]
        for team in self.teams:
            team.save()


class RequiresTeamEntriesTestCase(RequiresUsersTestCase,
                                  RequiresTournamentTestCase,
                                  RequiresTeamsTestCase):
    def setup_team_entries(self):
        self.setup_users()
        self.setup_teams()
        self.setup_tournament()

        self.team_entries = [
            models.TeamEntry(tournament=self.tournament, team=team)
            for team in self.teams
        ]

        for i, entry in enumerate(self.team_entries):
            entry.save()
            entry.players.add(self.users[2 * i])
            entry.players.add(self.users[2 * i + 1])
            entry.save()


class TournamentIsFFATestCase(RequiresTournamentTestCase):
    def setUp(self):
        self.setup_tournament()

    def test_is_ffa_property_returns_false_if_not_ffa(self):
        self.tournament.max_team_size = 3
        self.tournament.min_team_size = 1
        self.assertFalse(self.tournament.is_ffa)

    def test_is_ffa_property_returns_true_if_ffa(self):
        self.tournament.max_team_size = self.tournament.min_team_size = 1
        self.assertTrue(self.tournament.is_ffa)


class TournamentEnrolledNamesTestCase(RequiresTeamEntriesTestCase):
    def setUp(self):
        self.setup_team_entries()

    def test_enrolled_team_names_property(self):
        self.assertEqual(
            self.tournament.enrolled_team_names,
            [team.name for team in self.teams]
        )

    def test_enrolled_player_names_property(self):
        self.assertEqual(
            self.tournament.enrolled_player_names,
            [user.username for user in self.users]
        )
