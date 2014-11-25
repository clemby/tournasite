from datetime import datetime, timedelta

from django.http import Http404
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import mock

from . import models
from . import views


class RequiresUsersTestCase(TestCase):
    def create_user(self, **kwargs):
        user = User(**kwargs)
        user.save()
        return user

    def setup_users(self):
        self.users = [
            self.create_user(username='Test user {}'.format(i))
            for i in range(8)
        ]


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
    def create_team(self, **kwargs):
        team = models.Team(**kwargs)
        team.save()
        return team

    def setup_teams(self):
        user_range = range(len(self.users) / 2)

        self.teams = [
            self.create_team(
                name='Team {}'.format(i),
                creator=self.users[2 * i]
            )
            for i in user_range
        ]


class RequiresTeamEntriesTestCase(RequiresUsersTestCase,
                                  RequiresTournamentTestCase,
                                  RequiresTeamsTestCase):
    def create_team_entry(self, tournament, team, players=None):
        entry = models.TeamEntry(tournament=tournament, team=team)
        entry.save()

        if players:
            entry.players = players
            entry.save()

        return entry

    def setup_team_entries(self):
        self.setup_users()
        self.setup_teams()
        self.setup_tournament()

        self.team_entries = [
            self.create_team_entry(
                tournament=self.tournament,
                team=team,
                players=(self.users[2 * i], self.users[2 * i + 1])
            )
            for i, team in enumerate(self.teams)
        ]


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


class TournamentContainsPlayersTestCase(RequiresTeamEntriesTestCase):
    def setUp(self):
        self.setup_team_entries()

    def test_contains_player_returns_false_if_user_not_entered(self):
        user = self.create_user()
        self.assertFalse(self.tournament.contains_player(user))

    def test_contains_player_returns_true_if_user_has_entered(self):
        user = self.users[0]
        self.assertTrue(self.tournament.contains_player(user))


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
    def test_get_current_or_404_throws_404_if_None_found(self):

        with mock.patch.object(models.Tournament, 'get_current',
                               side_effect=lambda: None):
            self.assertRaises(
                Http404,
                models.Tournament.get_current_or_404
            )


class TeamGetCurrentMembersTestCase(RequiresUsersTestCase,
                                    RequiresTeamsTestCase,
                                    RequiresTournamentTestCase):
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


class TeamHasEnteredTournamentTestCase(RequiresTeamEntriesTestCase):
    def setUp(self):
        self.user = self.create_user()
        self.team = self.create_team(creator=self.user)
        self.setup_tournament()

    def test_team_has_entered_returns_false_if_no_entries(self):
        self.assertFalse(self.team.has_entered(self.tournament))

    def test_team_has_entered_returns_true_if_no_entries(self):
        self.create_team_entry(team=self.team, tournament=self.tournament)
        self.assertTrue(self.team.has_entered(self.tournament))


class ViewTestCase(TestCase):
    test_url = None

    def test_returns_200_status_code(self):
        # Don't run for this (abstract) class, as there's no test_url.
        if self.__class__ != ViewTestCase:
            response = self.client.get(self.test_url)
            self.assertEqual(response.status_code, 200)


class TournamentDetailViewTestCase(RequiresTeamEntriesTestCase, ViewTestCase):
    def setUp(self):
        self.setup_team_entries()
        self.test_url = reverse('tourn:tournament_detail',
                                args=(self.tournament.pk,))
        self.view = views.TournamentDetail()

        self.other_tournament = self.create_tournament(name='tournament 2')
        self.other_teams = [
            self.create_team(
                name='Other team {}'.format(i),
                creator=self.users[2 * i]
            )
            for i in range(len(self.teams))
        ]

        self.other_entries = [
            self.create_team_entry(
                tournament=self.other_tournament,
                team=team,
                players=(self.users[2 * i], self.users[2 * i + 1])
            )
            for i, team in enumerate(self.other_teams)
        ]

        self.other_matches = [
            models.Match(name='Other match', tournament=self.other_tournament)
        ]
        for match in self.other_matches:
            match.save()

    def test_get_team_list_only_uses_entries_from_that_tournament(self):
        team_objects = self.view.get_team_list(tournament=self.tournament)
        for team_obj in team_objects:
            self.assertFalse(team_obj['name'].startswith('Other'))

    def test_get_match_list_only_uses_entries_from_that_tournament(self):
        match_objects = self.view.get_match_list(tournament=self.tournament)
        for match_obj in match_objects:
            self.assertFalse(match_obj['name'].startswith('Other'))


class TournamentListTestCase(RequiresTournamentTestCase, ViewTestCase):
    test_url = reverse('tourn:tournament_list')

    def setUp(self):
        self.tournaments = [
            self.create_tournament(name='tournament {}'.format(i))
            for i in range(0, 4)
        ]
