from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden, HttpResponse
from cache.models import *
from django.views.decorators.csrf import csrf_exempt

from doi_cache.settings import ZOTERO_ENDPOINT, ZOTERO_API_KEY, ZOTERO_ENDPOINT_API_KEYS

import requests
import json, os, binascii

def fetch_metadata_by_doi(doi, record=None):
    headers = {'Accept':'application/vnd.citationstyles.csl+json'}
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

def check_pdf_urls(json_resp):
    for idx, item in enumerate(json_resp):
        new_attachments = []
        for attachment in item.get('attachments',[]):
            if attachment['mimeType'] == 'application/pdf':
                try:
                    rh = requests.head(attachment['url'],allow_redirects=True)
                    if 'pdf' in rh.headers.get('content-type', ''):
                        new_attachments.append(attachment)
                    else:
                        new_attachments.append(dict(rh.headers))
                except requests.exceptions.RequestException:
                    pass
            else:
                new_attachments.append(attachment)
        json_resp[idx]['attachments'] = new_attachments

    return json_resp

def fetch_zotero(url, record=None):
    headers = {'Content-Type': 'application/json'}
    json_resp = None
    try:
        url_req = requests.get(url)
        new_url = url_req.url
        zotero_data = {'url':new_url,
                'sessionid':binascii.hexlify(os.urandom(8)),
                'apikey':ZOTERO_API_KEY}
        r = requests.post(ZOTERO_ENDPOINT, headers=headers, data=json.dumps(zotero_data))
        json_resp = r.json()
        json_resp = check_pdf_urls(json_resp)

    except (ValueError, requests.exceptions.RequestException, TypeError):
        pass

    url = url[:MAX_URL_LENGTH]
    if record is None or record.url != url:
        record, created = ZoteroRecord.objects.get_or_create(url=url)
    record.body = json.dumps(json_resp)
    record.save()
    return json_resp



def get_doi(request, doi):
    if len(doi) >= MAX_DOI_LENGTH:
        raise Http404('Invalid DOI "'+doi+'"')
    doi = doi.lower()

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

def _get_batch(dois, verbose=False):
    dois = [doi.lower() for doi in dois]
    records_list = Record.objects.filter(doi__in=dois)
    records_dct = {r.doi:r for r in records_list}
    results = []
    for doi in dois:
        if verbose:
            print doi
        if doi in records_dct:
            body = records_dct[doi].body
            try:
                results.append(json.loads(body))
            except ValueError:
                results.append(None)
        else:
            results.append(fetch_metadata_by_doi(doi))
    return results

@csrf_exempt
def get_batch(request):
    try:
        ids = json.loads(request.POST.get("dois", "[]"))
        if len(ids) > MAX_BATCH_LENGTH:
            raise ValueError('DOI list is too long (length: %d, max: %d)' % (len(ids), MAX_BATCH_LENGTH))
        dois = [str(x)[:MAX_DOI_LENGTH] for x in ids]
        results = _get_batch(dois)
        # TODO: insert the records in one request
        return HttpResponse(json.dumps(results), content_type='application/json')

    except ValueError:
        return HttpResponse('Bad DOI list',status=400)

def get_zotero_doi(request, doi):
    if len(doi) >= MAX_DOI_LENGTH:
        raise Http404('Invalid DOI "'+doi+'"')
    doi = doi.lower()
    return get_zotero('http://doi.org/'+doi)

@csrf_exempt
def get_zotero_url(request):
    url = request.POST.get('url') or request.GET.get('url')
    key = request.POST.get('key') or request.GET.get('key')
    if not key:
        return HttpResponseForbidden('API key required')
    if key not in ZOTERO_ENDPOINT_API_KEYS:
        return HttpResponseForbidden('Invalid API key.')
    if not url:
        raise Http404('No URL provided')
    url = url[:MAX_URL_LENGTH]
    return get_zotero(url)

def get_zotero(url):
    # Look up DOI in database
    try:
        r = ZoteroRecord.objects.get(url=url)
        if r.is_fresh():
            return HttpResponse(r.body, content_type='application/json')
    except ZoteroRecord.DoesNotExist:
        pass

    metadata = fetch_zotero(url)
    if metadata is not None:
        return HttpResponse(json.dumps(metadata), content_type='application/json')
    else:
        return HttpResponse('null')

def get_count(request):
    count = Record.objects.count()
    return HttpResponse(str(count))

