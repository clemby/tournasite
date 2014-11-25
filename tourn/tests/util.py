from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User


from .. import models


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
