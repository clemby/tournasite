from django.views import generic

from .models import Event


class EventDetail(generic.DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventTimeline(generic.ListView):
    model = Event
    template_name = 'events/event_timeline.html'
    context_object_name = 'event_list'
