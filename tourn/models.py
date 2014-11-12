from django.http import Http404
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Tournament(models.Model):
    name = models.CharField(max_length=60, blank=True)

    min_team_size = models.SmallIntegerField(default=1)
    max_team_size = models.SmallIntegerField(default=2)

    min_teams_per_match = models.SmallIntegerField(default=2)
    max_teams_per_match = models.SmallIntegerField(default=2)

    planned_start = models.DateTimeField()
    planned_finish = models.DateTimeField(null=True)

    @classmethod
    def get_current(cls):
        future_tournaments = cls.objects.filter(
            planned_start__gte=timezone.now()
        )

        if future_tournaments.count():
            start = future_tournaments.aggregate(models.Min('planned_start'))
        else:
            start = cls.objects.exclude(
                planned_start__gt=timezone.now()
            ).aggregate(
                models.Max('planned_start')
            )

        if not start:
            return None

        start = start.values()[0]

        return cls.objects.filter(planned_start=start).first()

    @classmethod
    def get_current_or_404(cls):
        tournament = cls.get_current()
        if not tournament:
            raise Http404

        return tournament

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name

    @property
    def is_ffa(self):
        return self.max_team_size == 1

    @property
    def enrolled_names(self):
        return [tup[0] for tup in self.entries.values_list('team__name')]


class Team(models.Model):
    name = models.CharField(max_length=40, blank=False, unique=True)
    creator = models.ForeignKey(User, related_name='created_teams')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name

    def get_current_members(self):
        tournament = Tournament.get_current()
        try:
            entry = self.entries.get(tournament=tournament)
        except TeamEntry.DoesNotExist:
            return []
        return entry.players


class TeamEntry(models.Model):
    """
    Membership of a team, for a single tournament.

    Team membership differs between tournaments.
    """
    tournament = models.ForeignKey(Tournament, related_name='entries')
    players = models.ManyToManyField(User, related_name='tournament_entries')
    team = models.ForeignKey(Team, related_name='entries')


class Match(models.Model):
    name = models.CharField(max_length=40, blank=True)
    teams = models.ManyToManyField(Team, related_name='matches', null=True)
    winner = models.ForeignKey(Team, related_name='victories', null=True)
    tournament = models.ForeignKey(Tournament, related_name='matches')

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return '{}: {}'.format(self.tournament.name, self.name)

    def set_winner(self, winning_team):
        if winning_team not in self.teams:
            raise ValueError('Winning team is not in match')

        self.winner = winning_team
