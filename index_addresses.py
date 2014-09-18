import csv
import re
from elasticsearch import Elasticsearch

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
