# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20170417_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucscredentials',
            name='cred_password',
            field=models.CharField(max_length=255),
        ),
    ]
