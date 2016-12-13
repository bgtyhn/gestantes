# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appgestantes', '0009_auto_20161203_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='segundotrimestre',
            name='fecha_factores_riesgo',
            field=models.DateField(blank=True, null=True),
        ),
    ]
