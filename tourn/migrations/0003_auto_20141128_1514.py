# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0002_team_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='short_name',
            field=models.CharField(default=b'', max_length=12, blank=True),
        ),
    ]
