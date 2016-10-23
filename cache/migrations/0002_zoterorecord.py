# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cache', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoteroRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=4096)),
                ('fetched', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
