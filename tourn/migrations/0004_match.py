# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0003_auto_20141107_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('planned_start', models.DateTimeField(null=True)),
                ('planned_finish', models.DateTimeField(null=True)),
                ('subsequent', models.ForeignKey(related_name=b'predecessors', to='tourn.Match', null=True)),
                ('teams', models.ManyToManyField(related_name=b'matches', to='tourn.Team')),
                ('winner', models.ForeignKey(related_name=b'victories', to='tourn.Team', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
