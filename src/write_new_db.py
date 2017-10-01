import jsonlines
import sqlite3
import string
import sys

from collections import OrderedDict as odict

import db_handler


def get_record_info(record):
	# url_hash, record.items()
	record_data = list(record.values())[0]
	# record.update({field: str(value) for field, value in record_data.items() if value is None})
	field_names_string = ', '.join([str(field) for field in record_data.keys()])
	data = list(record_data.values())
	return field_names_string, data


def safetychecks(record):
	safe_chars = set(string.ascii_lowercase)
	safe_chars.update(['_', '_'])
	try:
		fields_chars = set(''.join([field for field in record.keys()]))
	except AttributeError:
		fields_chars = set(list(record))
	if fields_chars.issubset(safe_chars):
		return True
	else:
		print(fields_chars, record, '\n',
			'Browser Database tables have suspicious characters in field names. Please examine them.',
			'As a precaution against an SQL injection attack, only lowercase letters and underscore '
			'charaters are permitted in field names.',
			'Program halted.', sep='\n')
		sys.exit()


def make_queries(table, field_names, values):
	queries = {'create': '''CREATE TABLE {} ({})'''.format(table, field_names)}
	queries.update({'insert': "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table)})
	return queries


def create_table(cursor, query):
	try:
		cursor.execute(query)
	except sqlite3.OperationalError as excep:
		print(excep)


def insert_record(connection, cursor, query, data):
	cursor.execute(query, data)
	connection.commit()


def write_to_db(database, record, table='moz_places'):
	
	field_names_string, data = get_record_info(record)
	# table_name = ['moz_places']
	queries = make_queries(table, field_names_string, values=data)
	conn, cur, filepath = db_handler.connect_db(database)
	
	create_table(cursor=cur, query=queries['create'])
	insert_record(connection=conn, cursor=cur, query=queries['insert'], data=data)
	
	conn.close()
	

def write_to_json(json_path, record_yielder):
	with jsonlines.open(json_path, 'w') as json_records_obj:
		for record in record_yielder:
			json_records_obj.write(record)


def create_test_data():
	test_record = odict(
				{'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
				 'rev_host': 'gro.allizom.www.', 'visit_count': 0, 'hidden': 0, 'typed': 0,
				 'favicon_id': None, 'frecency': 76, 'last_visit_date': None, 'guid': 'NNqZA_f2KHI1',
				 'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
				 'preview_image_url': None
				 })
	return test_record


if __name__ == '__main__':
	test_record = create_test_data()
	write_to_db(database='test.sqlite', record=test_record)
