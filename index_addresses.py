import sys
import csv
import re
import os
from urlparse import urlparse
from elasticsearch import Elasticsearch

if os.environ.get('BONSAI_URL'):
  url = urlparse(os.environ['BONSAI_URL'])
  ELASTICSEARCH_HOST = url.hostname
  ELASTICSEARCH_AUTH = url.username + ':' + url.password
  es = Elasticsearch([{'host': ELASTICSEARCH_HOST}])
else:
  es = Elasticsearch(os.environ.get('ELASTICSEARCH_PORT'))

files_given = sys.argv
for file_name in files_given:
  if file_name == 'index_addresses.py':
    continue
  else:
    file_path = file_name
    print 'adding ' + file_path

    with open(file_path, 'r') as csvfile:
      print "open file"
      csv_reader = csv.DictReader(csvfile, fieldnames=[], restkey='undefined-fieldnames', delimiter=',')

      current_row = 0
      for row in csv_reader:
        current_row += 1
        if current_row == 1:
          csv_reader.fieldnames = row['undefined-fieldnames']
          continue
        address = row
        if current_row % 1000 == 0:
          print "%s addresses indexed" % current_row
        if re.match('\d+', address['PVANUM']):
          es.index(index='addresses', doc_type='address', id=address['PVANUM'], body={'PVANUM': address['PVANUM'], 'NUM1': address['NUM1'], 'NAME': address['NAME'], 'TYPE': address['TYPE'], 'ADDRESS': address['ADDRESS'], 'UNIT': address['UNIT'], 'X': address['X'], 'Y': address['Y']})

    csvfile.close()
