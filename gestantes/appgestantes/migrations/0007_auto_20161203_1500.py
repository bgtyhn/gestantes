# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-03 20:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appgestantes', '0006_auto_20161203_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='primertrimestre',
            old_name='factores_diabetes_fecha',
            new_name='fecha_factores_diabetes',
        ),
    ]