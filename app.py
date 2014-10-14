from collections import OrderedDict
import csv
import json
import os

from flask import Flask, render_template, jsonify, request, Response
from elasticsearch import Elasticsearch
from urlparse import urlparse

app = Flask(__name__)

@app.route('/')
def search_page():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if os.environ.get('BONSAI_URL'):
  url = urlparse(os.environ['BONSAI_URL'])
  bonsai_tuple = url.netloc.partition('@')
  ELASTICSEARCH_HOST = bonsai_tuple[2]
  ELASTICSEARCH_AUTH = bonsai_tuple[0]
  es = Elasticsearch([{'host': ELASTICSEARCH_HOST}], http_auth=ELASTICSEARCH_AUTH)
else:
  es = Elasticsearch()

def search_for(address):
  results = es.search(index="addresses", body={"query": {"query_string": {"default_field": "ADDRESS", "query": address.replace("/", " ")}}})
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
    temp_csv = open('tmp.csv', 'w')
    csv_writer = csv.writer(temp_csv)
    next(csv_reader, None) # skip headers
    outsideRows = OrderedDict

    outsideRows.append(csv_reader[0])

    for index, row in enumerate(csv_reader):
        ordered_row = ['%s' % (row[fieldname]) for fieldname in csv_reader.fieldnames]
        print 'geocoding number %s' % index
        address = row['ADDRESS']

        print 'address: %s' % address

        results = search_for(address)
        if results['total'] != 0:
          result = results['hits'][0]

          ordered_row.append(result['_source']['X'])
          ordered_row.append(result['_source']['Y'])

        outsideRows.append(ordered_row)

    def generate():
      for row in outsideRows:
        yield ','.join(row) + '\n'

    return Response(generate(), mimetype='text/csv')
  else:
    return 'attach file', 400

if __name__ == ('__main__'):
  app.run(debug=True)
