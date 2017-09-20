import sqlite3

from collections import OrderedDict as odict

import db_handler
import record_fetcher

def create_test_data():
	test_record = odict(
				{'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
				 'rev_host': 'gro.allizom.www.', 'visit_count': 0, 'hidden': 0, 'typed': 0,
				 'favicon_id': None, 'frecency': 76, 'last_visit_date': None, 'guid': 'NNqZA_f2KHI1',
				 'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
				 'preview_image_url': None
				 })
	return test_record


test_record = create_test_data()
test_record.update({field: str(value) for field, value in test_record.items() if value is None})
field_names = ', '.join([str(field) for field in test_record.keys()])
data = list(test_record.values())


print(field_names)
table_name = 'history'
query_create = '''CREATE TABLE {} ({})'''.format(table_name, field_names)
query_insert = "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)
conn, cur, filepath = db_handler.connect_db('test.sqlite')
try:
	cur.execute(query_create)
except sqlite3.OperationalError as excep:
	print(excep)

cur.execute(query_insert, data)

conn.commit()
# cur.execute('''SELECT * FROM {}'''.format(table_name))
# print(cur.description)

record_yielder = record_fetcher.yield_prepped_records(cursor=cur, table='history', filepath=filepath)
for record_ in record_yielder:
	print(record_)
	
conn.close()
