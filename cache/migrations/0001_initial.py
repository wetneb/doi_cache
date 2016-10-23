# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doi', models.CharField(unique=True, max_length=2048)),
                ('fetched', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
