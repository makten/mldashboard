# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 08:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_ucscredentials_ucssystem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ucssystem',
            old_name='ipAddress',
            new_name='name',
        ),
    ]