"""
Utilities for tournament-generating scripts.

"""
from __future__ import print_function
from __future__ import division

from django.utils import timezone
from django.contrib.auth.models import User

from tourn.models import Tournament, Team, TeamEntry, Match


def get_model_instance(cls, arg, defaults=None, arg_attr='name'):
    if isinstance(arg, cls):
        return arg

    tup = None

    if isinstance(arg, int):
        tup = cls.objects.get_or_create(**{
            'pk': arg,
            arg_attr: arg,
            'defaults': defaults,
        })

    elif isinstance(arg, str):
        tup = cls.objects.get_or_create(**{
            arg_attr: arg,
            'defaults': defaults,
        })

    if tup is None:
        raise ValueError("Can't convert value into instance", {
            'arg': arg,
            'cls': cls
        })

    return tup[0]


def get_team(team, defaults=None):
    return get_model_instance(Team, team, defaults=defaults)


def get_user(user):
    return get_model_instance(User, user, arg_attr='username')


def get_tournament(tournament):
    return get_model_instance(Tournament, tournament, defaults={
        'planned_start': timezone.datetime(2014, 01, 01),
        'planned_finish': timezone.datetime(2015, 12, 25),
    })


def get_match(tournament, name='', teams=None, winner_next=None,
              loser_next=None):

    match = Match.objects.get_or_create(
        tournament=tournament,
        name=name,
        defaults={
            'winner_next': winner_next,
            'loser_next': loser_next,
        }
    )[0]
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


def generate_tournament(
    teams,
    teams_per_match=2,
    first_round=None,
    tournament=None,
    planned_start=None,
    planned_finish=None,
    team_defaults=None,
):
    num_teams = len(teams)
    first_round_match_count = num_teams // teams_per_match

    print('Creating tournament...')
    if tournament is None:
        tournament = get_tournament(
            'Tournament {}'.format(Tournament.objects.count() + 1)
        )
    else:
        tournament = get_tournament(tournament)
    print('Created tournament')

    print('Entering teams...')
    entries = []
    team_objects = []
    if isinstance(teams, dict):
        for team, players in teams.items():
            team_obj = get_team(team, defaults=team_defaults)
            team_objects.append(team_obj)

            user_objects = [get_user(p) for p in players]

            entry = TeamEntry(team=team_obj, tournament=tournament)
            entry.save()
            entry.players = user_objects
            entry.save()
            entries.append(entry)

    else:
        for team in teams:
            team_obj = get_team(team, defaults=team_defaults)
            team_objects.append(team_obj)

            entry = TeamEntry(team=team_obj, tournament=tournament)
            entry.save()
            entries.append(entry)
    print('Entered teams')

    print('Adding matches...')
    previous_round = [get_match(tournament, name='Final')]

    current_round_id = 2

    while len(previous_round) < first_round_match_count:
        current_round = []
        for match in previous_round:
            current_round.extend([
                get_match(
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

    print('Setting up matches...')
    if not first_round:
        first_round = previous_round

    for i, match in enumerate(first_round):
        match.teams = team_objects[
            i * teams_per_match: (i + 1) * teams_per_match
        ]
        match.save()
    print('First round complete')

    print('Done!')

    return tournament
