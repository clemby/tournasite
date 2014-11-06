from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=40, blank=False)
    members = models.ManyToManyField(User, related_name='teams', null=False)

    class Meta:
        ordering = ('name',)
