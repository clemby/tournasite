from __future__ import print_function
from __future__ import division

from django.utils import timezone
from django.contrib.auth.models import User

from tourn.models import Tournament, Team, TeamEntry, Match


# Change these.
num_users = 16
users_per_team = 2
teams_per_match = 2

tournament_name = 'Tournament {}'.format(Tournament.objects.count() + 1)


# Don't change these.
num_teams = num_users // users_per_team
first_round_match_count = num_teams // teams_per_match


print('Getting users...')
users = [
    User.objects.get_or_create(username='User {}'.format(i))[0]
    for i in range(num_users)
]

for user in users:
    user.save()
print('Created/retrieved {} users'.format(len(users)))


def get_team(name, creator, admins=None):
    qs = Team.objects.filter(name=name)
    if qs.count():
        team = qs.first()
    else:
        team = Team(name=name, creator=creator)
        team.save()

    if admins:
        team.admins = admins

    team.save()
    return team

print('Getting teams...')
teams = [
    get_team(
        name='Team {}'.format(team_idx),
        creator=users[users_per_team * team_idx],
        admins=(users[users_per_team * team_idx],)
    )
    for team_idx in range(num_teams)
]
print('Created/retrieved {} teams'.format(len(teams)))


print('Getting tournament...')
tournament = Tournament(
    name=tournament_name,
    planned_start=timezone.datetime(2014, 01, 01),
    planned_finish=timezone.datetime(2015, 12, 25)
)
tournament.save()
print('Created tournament')


def add_entry(team, players, tournament):
    entry = TeamEntry(team=team, tournament=tournament)
    entry.save()
    entry.players = players
    entry.save()


print('Getting entries...')
for i, team in enumerate(teams):
    players = users[users_per_team * i:users_per_team * (i + 1)]
    add_entry(team=team, players=players, tournament=tournament)
print('Entered teams into tournament')


def add_match(tournament, name='', teams=None, winner_next=None,
              loser_next=None):
    try:
        match = Match.objects.get(name=name)
    except Match.DoesNotExist:
        match = Match(name=name, tournament=tournament,
                      winner_next=winner_next, loser_next=loser_next)
        match.save()

    must_save = False

    if teams:
        match.teams = teams
        must_save = True

    if winner_next and winner_next != match.winner_next:
        match.winner_next = winner_next
        must_save = True

    if loser_next and loser_next != match.loser_next:
        match.loser_next = loser_next
        must_save = True

    if must_save:
        match.save()
    return match


print('Adding matches...')
print('- added tier 1')
previous_round = [add_match(tournament, name='Final')]

current_round_id = 2

while len(previous_round) < first_round_match_count:
    global previous_round
    current_round = []
    for match in previous_round:
        current_round.extend([
            add_match(
                tournament,
                name='{}:{}'.format(match.name, i),
                winner_next=match
            )
            for i in range(2)
        ])
    print('- added {} matches to tier {}'.format(
        len(current_round), current_round_id))
    current_round_id += 1
    previous_round = current_round


print('Setting teams...')
for i, match in enumerate(previous_round):
    match.teams = teams[i * teams_per_match: (i + 1) * teams_per_match]
    match.save()
print('Teams are set up for first round')


def win_first_round():
    for match in previous_round:
        match.set_winner(match.teams[1])
        match.save()
