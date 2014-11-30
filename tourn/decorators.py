from django.shortcuts import Http404, render

from . import models


def open_tournament_registration_required(view_func):
    """
    Only allow a view involving a tournament if registration is open.

    Currently will allow registration if and only if the tournament hasn't
    started.
    """
    def wrapped(request, *args, **kwargs):
        tournament_pk = kwargs.get('tournament_pk') or \
            kwargs.get('tournament_id')

        if not tournament_pk:
            raise Http404("Tournament doesn't exist!")

        tournament = models.Tournament.objects.get(pk=tournament_pk)

        if tournament.has_started:
            return render(request, 'tourn/message.html', {
                'message':
                'Unfortunately that tournament has already started, and '
                'registration is closed!',
                'title': 'Registration closed',
            })

        return view_func(request, *args, **kwargs)

    return wrapped
