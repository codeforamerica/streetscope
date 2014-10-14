import csv
import re
import os
from urlparse import urlparse
from elasticsearch import Elasticsearch

if os.environ.get('BONSAI_URL'):
  url = urlparse(os.environ['BONSAI_URL'])
  bonsai_tuple = url.netloc.partition('@')
  ELASTICSEARCH_HOST = bonsai_tuple[2]
  ELASTICSEARCH_AUTH = bonsai_tuple[0]
  es = Elasticsearch([{'host': ELASTICSEARCH_HOST}], http_auth=ELASTICSEARCH_AUTH)
else:
  es = Elasticsearch()

with open('data/ParcelCentroids.csv', 'r') as csvfile:
  print "open file"
  csv_reader = csv.DictReader(csvfile, fieldnames=[], restkey='undefined-fieldnames', delimiter=',')

  current_row = 0
  for row in csv_reader:
    current_row += 1
    if current_row == 1:
      csv_reader.fieldnames = row['undefined-fieldnames']
      continue
    address = row
    if re.match('\d+', address['PVANUM']):
      es.index(index='addresses', doc_type='address', id=address['PVANUM'], body={'PVANUM': address['PVANUM'], 'NUM1': address['NUM1'], 'NAME': address['NAME'], 'TYPE': address['TYPE'], 'ADDRESS': address['ADDRESS'], 'UNIT': address['UNIT'], 'X': address['X'], 'Y': address['Y']})

csvfile.close()
