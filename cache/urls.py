# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from cache.views import *

urlpatterns = patterns('',
        url(r'^count$', get_count, name='get_count'),
        url(r'^batch$', get_batch, name='get_batch'),
        url(r'^(?P<doi>10\..*)', get_doi, name='get_doi'),
        url(r'^zotero/(?P<doi>10\..*)', get_zotero_doi, name='get_zotero_url'),
        url(r'^zotero/query', get_zotero_url, name='get_zotero_url'),
)

