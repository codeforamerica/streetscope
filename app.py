import json
from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
app = Flask(__name__)

@app.route('/')
def search_page():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

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

if __name__ == ('__main__'):
  app.run()
