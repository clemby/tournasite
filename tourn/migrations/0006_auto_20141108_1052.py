# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0005_auto_20141108_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='matches',
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(related_name=b'matches', default=1, to='tourn.Tournament'),
            preserve_default=False,
        ),
    ]
