# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cache.views import *

urlpatterns = patterns('',
        url(r'^batch$', get_batch, name='get_batch'),
        url(r'^(?P<doi>10\..*)', get_doi, name='get_doi'),
)

