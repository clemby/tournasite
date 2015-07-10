from django.views import generic
from django.shortcuts import render

from tourn.models import Tournament

from .models import Event


class EventDetail(generic.DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventTimeline(generic.ListView):
    template_name = 'events/event_timeline.html'

    def get(self, request):
        return render(request, self.template_name, {
            'event_list': Event.objects.all(),
            'tournament_list': Tournament.objects.all(),
        })
