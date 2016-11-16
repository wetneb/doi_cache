# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import timedelta
from datetime.date import today

MAX_DOI_LENGTH = 2048
MAX_BATCH_LENGTH = 512
MAX_URL_LENGTH = 4096

class Record(models.Model):
    doi = models.CharField(max_length=MAX_DOI_LENGTH, unique=True)
    fetched = models.DateTimeField(auto_now=True)
    body = models.TextField(null=True,blank=True)

    def is_fresh(self):
        return self.fetched + timedelta(days=150) > today()

class ZoteroRecord(models.Model):
    url = models.CharField(max_length=MAX_URL_LENGTH, unique=True)
    fetched = models.DateTimeField(auto_now=True)
    body = models.TextField(null=True,blank=True)

