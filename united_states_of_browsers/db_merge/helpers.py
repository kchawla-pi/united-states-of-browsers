# -*- encoding: utf-8 -*-
"""
Contains miscellaneous functions useful at various places.

Available functions:
 - safetychecks: Checks the names being inserted using string formatting for suspicious characters.
 - make_queries: Constructs the queries necessary for specific pruposes.
"""
import os
import string
import sys

from united_states_of_browsers.db_merge.imported_annotations import *


def safetychecks_deprecated(record: Union[Dict[Text, Dict], Iterable[Text]]) -> True:
	""" Checks the names being inserted using string formatting for suspicious characters.
	Prevents SQL injection attacks.
	Returns True or Exits the program.
	"""
	safe_chars = set(string.ascii_lowercase)
	safe_chars.update(['_'])
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


def make_queries(table: Text, field_names: Text) -> Dict:
	""" Constructs the queries necessary for specific pruposes.
	Returns them as dict['purpose': 'query']
	"""
	queries = {'create': '''CREATE TABLE {} ({})'''.format(table, field_names)}
	queries.update({'insert': "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table)})
	return queries
	
	
query_sanitizer = lambda query: ''.join([chr for chr in query if chr.isalnum() or chr in {'_'}])  #, '?', '(', ')', ','}])

filepath_from_another = lambda filename, filepath=__file__: os.path.realpath(os.path.join(os.path.dirname(filepath), filename))
