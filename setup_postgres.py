from collections import OrderedDict
import os

from postgres import Postgres

POSTGRES_URL = os.environ.get('POSTGRES_URL')

db = Postgres(POSTGRES_URL)

columns = OrderedDict()
columns['QUERY_ADDRESS'] = 'varchar 255'
columns['RETURNED_ADDRESS'] = 'varchar 255'
columns['ES_SCORE'] = 'float8'
columns['ES_LAT'] = 'float8'
columns['ES_LONG'] = 'float8'
columns['GOOG_LAT'] = 'float8'
columns['GOOG_LONG'] = 'float8'
columns['DISTANCE'] = 'float8'
columns['ES_GEOCODED_AT'] = 'timestamptz'
columns['GOOG_GEOCODED_AT'] = 'timestamptz'

columns_sql = ['%s %s' % (key, value) for key, value in columns.items()]
create_table_sql = 'CREATE TABLE geocoder (%s)' % ', '.join(columns_sql)
db.run(create_table_sql)
