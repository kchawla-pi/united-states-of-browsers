# -*- encoding: utf-8 -*-
import os
import sqlite3
import string
import sys

from annotations import *


def get_record_info(record: Dict) -> Tuple[str, Sequence]:
	'''
	Accepts dict of field name, field values.
	Returns str of comma-separated key names and data.
	'''

	record_data = list(record.values())[0]
	field_names_string = ', '.join([str(field) for field in record_data.keys()])
	data = list(record_data.values())
	return field_names_string, data


def safetychecks(record: dict) -> True:
	'''
	Checks the names being inserted using string formatting for suspicious characters.
	Prevents SQL injection attacks.
	Returns True or Exits the program.
	'''
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


def make_queries(table: str, field_names: str) -> Dict:
	'''
	Constructs the queries necessary for specific pruposes.
	Returns them as dict['purpose': 'query']
	'''
	queries = {'create': '''CREATE TABLE {} ({})'''.format(table, field_names)}
	queries.update({'insert': "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table)})
	return queries


def create_table(cursor: sqlite3.Connection.cursor, query: str, counter: int=0) -> True:
	'''
	Creates a table in the connected to database.
	Accepts the connection.cursor object, creation query.
	Returns True or prints exception.
	'''
	try:
		cursor.execute(query)
		return True
	except sqlite3.OperationalError as excep:
		print(excep)


def insert_record(connection: sqlite3.Connection, cursor: sqlite3.Connection.cursor, query: str, data: Sequence) -> None:
	'''
	Commits a new record in to the database.
	Accepts connection object and cursor, insertion query and data.
	'''
	cursor.execute(query, data)
	connection.commit()


filepath_from_another = lambda filename, filepath=__file__: os.path.realpath(os.path.join(os.path.dirname(filepath), filename))
