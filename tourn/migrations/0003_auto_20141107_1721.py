# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0002_team_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(related_name=b'created_teams', to=settings.AUTH_USER_MODEL),
        ),
    ]
