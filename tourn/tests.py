from datetime import datetime
from django.http import Http404

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

import mock

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
    def create_tournament(self, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'test tournament'

        if 'planned_start' not in kwargs:
            kwargs['planned_start'] = timezone.now()

        tournament = models.Tournament(**kwargs)
        tournament.save()
        return tournament

    def setup_tournament(self, **kwargs):
        self.tournament = self.create_tournament(**kwargs)


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


class TournamentGetCurrentTestCase(RequiresTournamentTestCase):
    def setup_tournaments(self):
        self.dates = [
            datetime(2014, 1, 1),
            datetime(2014, 2, 1),
            datetime(2014, 3, 1),
            datetime(2014, 4, 1),
            datetime(2014, 5, 1),
        ]

        self.tournaments = [
            self.create_tournament(planned_start=date)
            for date in self.dates
        ]

    @mock.patch('django.utils.timezone.now',
                mock.Mock(side_effect=lambda: datetime(2014, 3, 1)))
    def test_get_current_gets_closest_future_tournament(self):
        self.setup_tournaments()
        self.assertEqual(
            models.Tournament.get_current(),
            self.tournaments[2]
        )

    @mock.patch('django.utils.timezone.now',
                mock.Mock(side_effect=lambda: datetime(2014, 6, 1)))
    def test_get_current_returns_most_recent_if_no_future_tournaments(self):
        self.setup_tournaments()
        self.assertEqual(
            models.Tournament.get_current(),
            self.tournaments[-1]
        )

    @mock.patch('django.utils.timezone.now',
                mock.Mock(side_effect=lambda: datetime(2014, 1, 1)))
    def test_get_current_returns_none_if_no_future_or_past(self):
        self.assertEqual(models.Tournament.get_current(), None)


class TournamentGetCurrentOr404TestCase(RequiresTournamentTestCase):
    def test_get_current_or_404_gets_current_if_possible(self):
        tournament = models.Tournament(
            name='tournament',
            planned_start=datetime(2014, 1, 1)
        )

        with mock.patch.object(models.Tournament, 'get_current',
                               side_effect=lambda: tournament):
            self.assertEqual(
                models.Tournament.get_current_or_404(),
                tournament
            )

    @mock.patch('tourn.models.Tournament.get_current',
                mock.Mock(side_effect=lambda: None))
    def test_get_current_or_404_throws_404_if_none_found(self):

        with mock.patch.object(models.Tournament, 'get_current',
                               side_effect=lambda: None):
            self.assertRaises(
                Http404,
                models.Tournament.get_current_or_404
            )
