# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-12-10 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisChannel', '0005_auto_20171210_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='contactRemarks',
            field=models.TextField(blank=True, null=True, verbose_name='设备的备注'),
        ),
    ]
