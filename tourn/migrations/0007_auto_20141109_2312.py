# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tourn', '0006_auto_20141108_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('players', models.ManyToManyField(related_name=b'memberships', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(related_name=b'+', to='tourn.Tournament')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='team',
            name='members',
        ),
    ]
