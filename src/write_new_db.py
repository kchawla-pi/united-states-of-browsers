import sqlite3
import string
import sys

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


def preprocess_record(record):
	record.update({field: str(value) for field, value in record.items() if value is None})
	field_names = ', '.join([str(field) for field in record.keys()])
	data = list(record.values())
	return field_names, data


def safetychecks(record):
	safe_chars = set(string.ascii_lowercase)
	safe_chars.update(['_', ' '])
	fields_chars = set(''.join([field for field in record.keys()]))
	if fields_chars.issubset(safe_chars):
		return True
	else:
		return False


def make_queries(table_name, field_names, values):
	queries = {'create': '''CREATE TABLE {} ({})'''.format(table_name, field_names)}
	queries.update({'insert': "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table_name)})
	return queries


def create_table(cursor, query):
	try:
		cursor.execute(query)
	except sqlite3.OperationalError as excep:
		print(excep)


def insert_record(connection, cursor, query, data):
	cursor.execute(query, data)
	connection.commit()


def write_to_db():
	test_record = create_test_data()
	if not safetychecks(test_record):
		print('Browser Database tables have suspicious characters in field names. Please examine them.',
		      'As a precaution against an SQL injection attack, only lowercase letters, space and hyphen'
		      'charaters are permitted in field names.',
		      'Program halted.', sep='\n')
		sys.exit()
	field_names, data = preprocess_record(test_record)
	table_name = 'history'
	queries = make_queries(table_name, field_names, values=data)
	conn, cur, filepath = db_handler.connect_db('test.sqlite')
	
	create_table(cursor=cur, query=queries['create'])
	insert_record(connection=conn, cursor=cur, query=queries['insert'], data=data)
	record_yielder = record_fetcher.yield_prepped_records(cursor=cur, table=table_name, filepath=filepath)
	
	for record_ in record_yielder:
		print(len(record_))
		
	conn.close()


if __name__ == '__main__':
	write_to_db()
