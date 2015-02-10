from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=40, blank=True)
    description = models.CharField(max_length=200, blank=True)

    start = models.DateTimeField()
    finish = models.DateTimeField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
