# doi_cache

Simple cached DOI metadata resolver with batch lookup capabilities.
This resolves metadata for articles, using CrossRef's API.
It adds a batch lookup capability, to retrieve many DOIs in a single request. This is particularly efficient if the DOIs have been cached before.

Usage:
<pre>
python manage.py runserver &
</pre>
For a single DOI:
<pre>
curl http://localhost:8000/10.1016/j.physletb.2015.01.010
</pre>
For a batch:

<pre>
curl -d 'dois=["10.1016/j.physletb.2015.01.010","10.5380/dp.v1i1.1922","10.1007/978-3-319-10936-7_9"]' http://localhost:8000/batch
</pre>

