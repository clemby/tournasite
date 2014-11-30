from datetime import datetime, timedelta

import mock
from django.test import TestCase
from django.http import Http404

from .. import models
from . import util as testutil


class TournamentIsFFATestCase(testutil.RequiresTournamentTestCase):
    def setUp(self):
        self.setup_tournament()

    def test_is_ffa_property_returns_false_if_not_ffa(self):
        self.tournament.max_team_size = 3
        self.tournament.min_team_size = 1
        self.assertFalse(self.tournament.is_ffa)

    def test_is_ffa_property_returns_true_if_ffa(self):
        self.tournament.max_team_size = self.tournament.min_team_size = 1
        self.assertTrue(self.tournament.is_ffa)


class TournamentEnrolledNamesTestCase(testutil.RequiresTeamEntriesTestCase):
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


class TournamentContainsPlayersTestCase(testutil.RequiresTeamEntriesTestCase):
    def setUp(self):
        self.setup_team_entries()

    def test_contains_player_returns_false_if_user_not_entered(self):
        user = self.create_user()
        self.assertFalse(self.tournament.contains_player(user))

    def test_contains_player_returns_true_if_user_has_entered(self):
        user = self.users[0]
        self.assertTrue(self.tournament.contains_player(user))


class TournamentGetCurrentTestCase(testutil.RequiresTournamentTestCase):
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
                mock.Mock(side_effect=lambda: datetime(2014, 3, 1)))
    def test_get_current_does_not_exclude_if_planned_finish_is_in_future(self):
        self.setup_tournaments()

        for t in self.tournaments:
            # Each tournament takes two weeks.
            t.planned_finish = t.planned_start + timedelta(14, 0, 0)
            t.save()

        self.assertEqual(
            models.Tournament.get_current(),
            self.tournaments[2]
        )

    @mock.patch('django.utils.timezone.now',
                mock.Mock(side_effect=lambda: datetime(2014, 3, 1)))
    def test_get_current_excludes_if_planned_finish_is_past(self):
        self.setup_tournaments()

        for t in self.tournaments[:-1]:
            t.planned_finish = t.planned_start
            t.save()

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
    def test_get_current_returns_None_if_no_future_or_past(self):
        self.assertEqual(models.Tournament.get_current(), None)


class TournamentGetCurrentOr404TestCase(testutil.RequiresTournamentTestCase):
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
    def test_get_current_or_404_throws_404_if_None_found(self):

        with mock.patch.object(models.Tournament, 'get_current',
                               side_effect=lambda: None):
            self.assertRaises(
                Http404,
                models.Tournament.get_current_or_404
            )


class TournamentHasStartedTestCase(TestCase):
    def setUp(self):
        self.tournament = models.Tournament(
            name='tournament',
            planned_start=datetime(2014, 1, 1)
        )

    @mock.patch('django.utils.timezone.now',
                mock.Mock(side_effect=lambda: datetime(2014, 2, 1)))
    def test_has_started_returns_true_if_planned_start_in_past(self):
        self.assertTrue(self.tournament.has_started)

    @mock.patch('django.utils.timezone.now',
                mock.Mock(side_effect=lambda: datetime(2013, 1, 1)))
    def test_has_started_returns_false_if_planned_start_not_in_past(self):
        self.assertFalse(self.tournament.has_started)


class TeamGetCurrentMembersTestCase(testutil.RequiresUsersTestCase,
                                    testutil.RequiresTeamsTestCase,
                                    testutil.RequiresTournamentTestCase):
    def setUp(self):
        self.setup_users()

        self.entered_tournaments = [
            self.create_tournament()
            for i in range(1, 4)
        ]

        self.unentered_tournament = self.create_tournament()

        self.team = self.create_team(name='Team', creator=self.users[0])
        self.team.save()

        self.entries = [
            models.TeamEntry(tournament=tournament, team=self.team)
            for tournament in self.entered_tournaments
        ]

        for i, entry in enumerate(self.entries):
            entry.save()
            entry.players = self.users[2 * i: 2 * i + 2]
            entry.save()

    def test_current_members(self):
        with mock.patch.object(
            models.Tournament,
            'get_current',
            side_effect=lambda: self.entered_tournaments[2]
        ):
            self.assertEqual(
                list(self.team.current_members.all()),
                [self.users[4], self.users[5]]
            )

    def test_current_members_is_None_if_no_entries_in_current_tournament(self):
        with mock.patch.object(
            models.Tournament,
            'get_current',
            side_effect=lambda: self.unentered_tournament
        ):
            self.assertEqual(
                self.team.current_members,
                None
            )

    def test_current_member_names(self):
        with mock.patch.object(
            models.Tournament,
            'get_current',
            side_effect=lambda: self.entered_tournaments[2]
        ):
            self.assertEqual(
                self.team.current_member_names,
                [self.users[4].username, self.users[5].username]
            )


class TeamHasEnteredTournamentTestCase(testutil.RequiresTeamEntriesTestCase):
    def setUp(self):
        self.user = self.create_user()
        self.team = self.create_team(creator=self.user)
        self.setup_tournament()

    def test_team_has_entered_returns_false_if_no_entries(self):
        self.assertFalse(self.team.has_entered(self.tournament))

    def test_team_has_entered_returns_true_if_no_entries(self):
        self.create_team_entry(team=self.team, tournament=self.tournament)
        self.assertTrue(self.team.has_entered(self.tournament))
