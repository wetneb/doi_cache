from django.shortcuts import render
from django.http import Http404, HttpResponse
from cache.models import *
from django.views.decorators.csrf import csrf_exempt

import requests
import json

def fetch_metadata_by_doi(doi, record=None):
    headers = {'Accept':'application/citeproc+json'}
    try:
        req = requests.get('http://dx.doi.org/'+doi, headers=headers)
        json_data = req.json()
        metadata = req.text
        if record is None or record.doi != doi:
            record, created = Record.objects.get_or_create(doi=doi)
        record.body = metadata
        record.save()
        return json_data
    except ValueError, requests.exceptions.RequestException:
        return None

def get_doi(request, doi):
    if len(doi) >= MAX_DOI_LENGTH:
        raise Http404('Invalid DOI "'+doi+'"')

    # Look up DOI in database
    try:
        r = Record.objects.get(doi=doi)
        return HttpResponse(r.body, content_type='application/json')
    except Record.DoesNotExist:
        metadata = fetch_metadata_by_doi(doi)
        if metadata is not None:
            return HttpResponse(json.dumps(metadata), content_type='application/json')
        else:
            return HttpResponse('null')

@csrf_exempt
def get_batch(request):
    try:
        ids = json.loads(request.POST.get("dois", "[]"))
        if len(ids) > MAX_BATCH_LENGTH:
            raise ValueError('DOI list is too long (length: %d, max: %d)' % (len(ids), MAX_BATCH_LENGTH))
        dois = [str(x)[:MAX_DOI_LENGTH] for x in ids]
        records_list = Record.objects.filter(doi__in=dois)
        records_dct = {r.doi:r for r in records_list}
        results = []
        for doi in dois:
            if doi in records_dct:
                body = records_dct[doi].body
                try:
                    results.append(json.loads(body))
                except ValueError:
                    results.append(None)
            else:
                results.append(fetch_metadata_by_doi(doi))
        # TODO: insert the records in one request
        return HttpResponse(json.dumps(results), content_type='application/json')

    except ValueError:
        return HttpResponse('Bad DOI list',status=400)

