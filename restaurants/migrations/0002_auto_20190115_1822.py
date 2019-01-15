# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-15 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishes',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('restaurant', 'dish')]),
        ),
    ]