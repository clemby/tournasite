# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('start', models.DateTimeField()),
                ('finish', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
