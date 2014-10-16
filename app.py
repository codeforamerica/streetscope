from collections import OrderedDict
import csv
import json
import os
from flask import Flask, render_template, jsonify, request, Response
from elasticsearch import Elasticsearch
from urlparse import urlparse

app = Flask(__name__)

RECORD_REQUESTS = os.environ.get('RECORD_REQUESTS', True)
POSTGRES_URL = os.environ.get('DATABASE_URL')

if RECORD_REQUESTS == True:
  from postgres import Postgres
  db = Postgres(POSTGRES_URL)

if os.environ.get('BONSAI_URL'):
  url = urlparse(os.environ['BONSAI_URL'])
  bonsai_tuple = url.netloc.partition('@')
  ELASTICSEARCH_HOST = bonsai_tuple[2]
  ELASTICSEARCH_AUTH = bonsai_tuple[0]
  es = Elasticsearch([{'host': ELASTICSEARCH_HOST}], http_auth=ELASTICSEARCH_AUTH)
else:
  es = Elasticsearch()

app = Flask(__name__)

@app.route('/')
def search_page():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

def record_geocode_request(query, returned, es_score, es_lat, es_long):
  if RECORD_REQUESTS == True:
    db.run("INSERT INTO geocoder VALUES (%s, %s, %s, %s, %s, NULL, NULL, NULL, NOW(), NULL)", (query, returned, es_score, es_lat, es_long))
  else:
    pass

def search_for(address):
  results = es.search(index="addresses", body={"query": {"query_string": {"default_field": "ADDRESS", "query": address.replace("/", " ")}}})
  if results['hits']['total'] != 0:
    hit = results['hits']['hits'][0]
    returned = hit['_source']['ADDRESS']
    es_score = hit['_score']
    es_lat = hit['_source']['X']
    es_long = hit['_source']['Y']
  else:
    returned = 'NULL'
    es_score = 'NULL'
    es_lat = 'NULL'
    es_long = 'NULL'

  record_geocode_request(address, returned, es_score, es_lat, es_long)

  return results['hits']

def format_parcel(match):
  return {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [
        float(match['X']),
        float(match['Y'])
      ]
    },
    "properties": {
      "formatted_address": match['ADDRESS'],
      "parcel_id": match['PVANUM']
    }
  }

def likely_parcels(query = '123 Main St'):
  hits = search_for(query)
  response = {
    "type": "FeatureCollection",
    "features": []
  }
  if hits["total"] == 0:
    return response
  for hit in hits['hits']:
    match = hit['_source']
    response['features'].append(format_parcel(match))
  return response

@app.route('/geocode')
def geocode():
  query = request.args['query']
  return jsonify(likely_parcels(query))

@app.route('/geocode_batch', methods=['POST'])
def geocode_batch():
  input_file = request.files.get('query', False)
  geocoded = {}
  if input_file is not False:
    csv_reader = csv.DictReader(input_file)
    all_rows = []

    for index, row in enumerate(csv_reader):
      ordered_row = OrderedDict()
      for fieldname in csv_reader.fieldnames:
        ordered_row[fieldname] = row[fieldname]
      address = row['ADDRESS']

      results = search_for(address)
      if results['total'] != 0:
        result = results['hits'][0]

        ordered_row['X'] = result['_source']['X']
        ordered_row['Y'] = result['_source']['Y']

      all_rows.append(ordered_row)

    def generate():
      for index, row in enumerate(all_rows):
        if index == 0: # for the first row make headers
          yield ','.join(row.keys()) + '\n'
        yield ','.join(row.values()) + '\n'

    input_filename = input_file.filename.split('.')[0]
    return Response(generate(), mimetype='text/csv',
      headers = {'Content-Disposition': 'attachment; filename=%s-geocoded.csv' % input_filename})
  else:
    return 'attach file', 400

if __name__ == ('__main__'):
  app.run(debug=True)
