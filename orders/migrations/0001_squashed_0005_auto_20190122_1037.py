# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-22 11:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [(b'orders', '0001_initial'), (b'orders', '0002_auto_20190116_1748'), (b'orders', '0003_auto_20190116_1753'), (b'orders', '0004_auto_20190120_1708'), (b'orders', '0005_auto_20190122_1037')]

    initial = True

    dependencies = [
        ('restaurants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(1, 'in progress'), (2, 'accepted'), (3, 'dispatched'), (4, 'delivered'), (5, 'cancelled'), (6, 'rejected')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='order quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_detail', to='orders.Order')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_order', to='restaurants.Menu')),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='updated_at',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetail',
            unique_together=set([('item', 'order')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'placed'), (2, 'in progress'), (1, 'accepted'), (3, 'dispatched'), (4, 'delivered'), (5, 'cancelled'), (6, 'rejected')], default=0),
        ),
    ]