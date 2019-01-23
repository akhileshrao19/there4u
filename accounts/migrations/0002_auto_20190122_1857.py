# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-22 18:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_squashed_0003_auto_20190122_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.City'),
        ),
        migrations.AlterField(
            model_name='user',
            name='pin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.Pin'),
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.State'),
        ),
    ]