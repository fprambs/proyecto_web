# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrendados', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=45)),
            ],
        ),
    ]
