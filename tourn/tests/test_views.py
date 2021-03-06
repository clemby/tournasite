from django.core.urlresolvers import reverse

from .. import models
from .. import views
from .. import forms

from . import util as testutil


class ViewTestCase(object):
    test_url = None

    def test_returns_200_status_code(self):
        # Don't run for this (abstract) class, as there's no test_url.
        if self.__class__ != ViewTestCase and self.test_url is not False:
            response = self.client.get(self.test_url)
            self.assertEqual(response.status_code, 200)


class TournamentDetailViewTestCase(testutil.RequiresTeamEntriesTestCase,
                                   ViewTestCase):
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


class TournamentListTestCase(testutil.RequiresTournamentTestCase,
                             ViewTestCase):
    test_url = reverse('tourn:tournament_list')

    def setUp(self):
        self.tournaments = [
            self.create_tournament(name='tournament {}'.format(i))
            for i in range(0, 4)
        ]


class PlayerSignupMixinTestCase(testutil.RequiresTeamEntriesTestCase,
                                ViewTestCase):
    test_url = False

    def setUp(self):
        self.setup_tournament()
        self.setup_team_entries()
        self.mixin = views.TeamSignupMixin()

    def test_get_team_signup_form_or_none_returns_none_if_no_teams(self):
        self.assertEqual(
            self.mixin.get_team_signup_form_or_none(
                player_pk=self.users[0].pk,
                tournament_pk=self.tournament.pk
            ),
            None
        )

    def test_get_team_signup_form_or_none_returns_form_if_teams(self):
        self.teams[0].admins.add(self.users[0])
        self.assertIsInstance(
            self.mixin.get_team_signup_form_or_none(
                player_pk=self.users[0].pk,
                tournament_pk=self.tournament.pk
            ),
            forms.TeamEntryForm
        )


class TeamSignupMixinTestCase(testutil.RequiresTeamEntriesTestCase,
                              ViewTestCase):
    test_url = False

    def setUp(self):
        self.setup_tournament()
        self.setup_team_entries()
        self.mixin = views.TeamSignupMixin()

    def test_get_team_signup_form_or_none_returns_none_if_no_teams(self):
        self.assertEqual(
            self.mixin.get_team_signup_form_or_none(
                player_pk=self.users[0].pk,
                tournament_pk=self.tournament.pk
            ),
            None
        )

    def test_get_team_signup_form_or_none_returns_form_if_teams(self):
        self.teams[0].admins.add(self.users[0])
        self.assertIsInstance(
            self.mixin.get_team_signup_form_or_none(
                player_pk=self.users[0].pk,
                tournament_pk=self.tournament.pk
            ),
            forms.TeamEntryForm
        )
