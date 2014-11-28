# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('loser_next', models.ForeignKey(related_name=b'received_losers', blank=True, to='tourn.Match', help_text=b'Losers will progress to the chosen match', null=True)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerRandomTeamEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(related_name=b'tournament_random_team_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Single player entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('admins', models.ManyToManyField(related_name=b'administered_teams', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(related_name=b'created_teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('players', models.ManyToManyField(related_name=b'tournament_entries', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(related_name=b'entries', to='tourn.Team')),
            ],
            options={
                'verbose_name_plural': 'Team entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, blank=True)),
                ('min_team_size', models.SmallIntegerField(default=1)),
                ('max_team_size', models.SmallIntegerField(default=2)),
                ('min_teams_per_match', models.SmallIntegerField(default=2)),
                ('max_teams_per_match', models.SmallIntegerField(default=2)),
                ('planned_start', models.DateTimeField()),
                ('planned_finish', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='teamentry',
            name='tournament',
            field=models.ForeignKey(related_name=b'entries', to='tourn.Tournament'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='teamentry',
            unique_together=set([('tournament', 'team')]),
        ),
        migrations.AddField(
            model_name='playerrandomteamentry',
            name='tournament',
            field=models.ForeignKey(related_name=b'player_entries', to='tourn.Tournament'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='playerrandomteamentry',
            unique_together=set([('tournament', 'player')]),
        ),
        migrations.AddField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(related_name=b'matches', null=True, to='tourn.Team', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(related_name=b'matches', to='tourn.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(related_name=b'victories', blank=True, to='tourn.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='winner_next',
            field=models.ForeignKey(related_name=b'received_winners', blank=True, to='tourn.Match', help_text=b'Winners will progress to the chosen match', null=True),
            preserve_default=True,
        ),
    ]
