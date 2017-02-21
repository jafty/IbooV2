# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_message_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('DM', 'Demande'), ('RE', 'Refus'), ('AC', 'Accept')], default='DM', max_length=2),
        ),
    ]