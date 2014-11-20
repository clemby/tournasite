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
            planned_finish__gte=timezone.now()
        )

        if future_tournaments.exists():
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
    def enrolled_team_names(self):
        return [tup[0] for tup in self.entries.values_list('team__name')]

    @property
    def enrolled_player_names(self):
        values_list = self.entries.values_list('players__username')
        return [tup[0] for tup in values_list]


class Team(models.Model):
    name = models.CharField(max_length=40, blank=False, unique=True)
    creator = models.ForeignKey(User, related_name='created_teams')
    admins = models.ManyToManyField(User, related_name='administered_teams')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name

    @property
    def current_members(self):
        tournament = Tournament.get_current()
        try:
            entry = self.entries.get(tournament=tournament)
        except TeamEntry.DoesNotExist:
            return None
        return entry.players

    @property
    def current_member_names(self):
        values_list = self.current_members.values_list('username')
        return [tup[0] for tup in values_list]

    def is_admin(self, user):
        try:
            self.admins.get(pk=user.pk)
        except:
            return False
        return True


class TeamEntry(models.Model):
    """A team's entry into a tournament."""
    tournament = models.ForeignKey(Tournament, related_name='entries')
    players = models.ManyToManyField(User, related_name='tournament_entries')
    team = models.ForeignKey(Team, related_name='entries')

    def get_member_names(self):
        return [tup[0] for tup in self.players.values_list('username')]


class PlayerRandomTeamEntry(models.Model):
    """
    A Player's request to join a random team in a tournament.
    """
    tournament = models.ForeignKey(Tournament, related_name='player_entries')
    player = models.ForeignKey(
        User, related_name='tournament_random_team_entries')


class Match(models.Model):
    name = models.CharField(max_length=40, blank=True)
    teams = models.ManyToManyField(Team, related_name='matches', null=True)
    winner = models.ForeignKey(Team, related_name='victories', null=True)
    tournament = models.ForeignKey(Tournament, related_name='matches')
    winner_next = models.ForeignKey('self', related_name='received_winners',
                                    null=True)
    loser_next = models.ForeignKey('self', related_name='received_losers',
                                   null=True)

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return '{}: {}'.format(self.tournament.name, self.name)

    def set_winner(self, winning_team):
        try:
            self.teams.get(pk=winning_team.pk)
        except Team.DoesNotExist:
            raise ValueError(
                'Winning team {} is not in match'.format(winning_team.name))

        self.winner = winning_team

        if self.winner_next:
            self.winner_next.teams.add(winning_team)

        if self.loser_next:
            losing_teams = self.loser_next.teams

            for team in self.teams.all():
                if team != winning_team:
                    losing_teams.add(team)

        self.save()
