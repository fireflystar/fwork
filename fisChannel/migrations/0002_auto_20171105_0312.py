# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-04 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fisChannel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tongdao',
            name='shebeiPoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fisChannel.shebei', verbose_name='设备'),
        ),
    ]
