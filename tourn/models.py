from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=40, blank=False)
    members = models.ManyToManyField(User, related_name='teams')
    creator = models.ForeignKey(User, related_name='created_teams')

    class Meta:
        ordering = ('name',)

    def unicode(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=60, blank=True)

    min_team_size = models.SmallIntegerField(default=1)
    max_team_size = models.SmallIntegerField(default=2)

    min_teams_per_match = models.SmallIntegerField(default=2)
    max_teams_per_match = models.SmallIntegerField(default=2)

    def unicode(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name


class Match(models.Model):
    name = models.CharField(max_length=40, blank=True)
    teams = models.ManyToManyField(Team, related_name='matches', null=True)
    winner = models.ForeignKey(Team, related_name='victories', null=True)
    tournament = models.ForeignKey(Tournament, related_name='matches')

    def unicode(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name

    def set_winner(self, winning_team):
        if winning_team not in self.teams:
            raise ValueError('Winning team is not in match')

        self.winner = winning_team
