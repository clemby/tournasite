# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0004_match'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, blank=True)),
                ('min_team_size', models.SmallIntegerField(default=1)),
                ('max_team_size', models.SmallIntegerField(default=2)),
                ('min_teams_per_match', models.SmallIntegerField(default=2)),
                ('max_teams_per_match', models.SmallIntegerField(default=2)),
                ('matches', models.ForeignKey(to='tourn.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='match',
            name='planned_finish',
        ),
        migrations.RemoveField(
            model_name='match',
            name='planned_start',
        ),
        migrations.RemoveField(
            model_name='match',
            name='subsequent',
        ),
        migrations.AlterField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(related_name=b'matches', null=True, to=b'tourn.Team'),
        ),
    ]
