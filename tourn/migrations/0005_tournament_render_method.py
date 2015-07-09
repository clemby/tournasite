# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0004_auto_20141204_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='render_method',
            field=models.SmallIntegerField(default=2, choices=[(2, b'jQuery Bracket'), (1, b'Bootstrap')]),
            preserve_default=True,
        ),
    ]
