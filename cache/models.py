# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

MAX_DOI_LENGTH = 2048

class Record(models.Model):
    doi = models.CharField(max_length=MAX_DOI_LENGTH, unique=True)
    fetched = models.DateTimeField(auto_now=True)
    body = models.TextField(null=True,blank=True)


