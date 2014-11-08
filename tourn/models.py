from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=40, blank=False)
    members = models.ManyToManyField(User, related_name='teams')
    creator = models.ForeignKey(User, related_name='created_teams')

    class Meta:
        ordering = ('name',)


class Match(models.Model):
    name = models.CharField(max_length=40, blank=True)
    teams = models.ManyToManyField(Team, related_name='matches', null=True)
    winner = models.ForeignKey(Team, related_name='victories', null=True)

    def set_winner(self, winning_team):
        if winning_team not in self.teams:
            raise ValueError('Winning team is not in match')

        self.winner = winning_team
