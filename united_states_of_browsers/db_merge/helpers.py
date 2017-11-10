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


def make_queries(table: Text, fieldnames: Text) -> Dict:
	""" Constructs the queries necessary for specific pruposes.
	Returns them as dict['purpose': 'query']
	"""
	queries = {'create': f'''CREATE TABLE {table} (id INT PRIMARY KEY , {fieldnames})'''}
	queries.update({'insert': f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"})
	return queries
	

def incrementer(start: int=0) -> Generator[int, None, None]:
	"""	Infinite Generator which yields integer value, incremented by +1 every time it is used
	Accepts a start value, default is 0.
	
	Usage: inc = incrementer(0); next(inc)
	"""
	next = start
	yield next
	while True:
		next += 1
		yield next


def query_sanitizer(query: str, exceptions: Union[str, Iterable]='_') -> str:
	""" Removes non-alphanumeric characters from a query.
	Retains characters passed in as exceptions. (Default: '_')
	Returns a string.
	"""
	exceptions = set(exceptions)
	return ''.join([char for char in query if char.isalnum() or char in exceptions])  #, '?', '(', ')', ','}])


def retrieve_record(db_path: PathInfo, key: Union[Text, int, Iterable[Union[Text, int]]], key_type: Union['id', 'guid', 'hash']
                    ) -> NamedTuple:
	""" Returns the record from a database based on the provided key.
	Accepts the database's path and the key value.
	Optionally, accepts key type. Options: 'id' (default), 'guid', 'hash'
	"""
	import sqlite3
	# key = [str(key_element) for key_element in [key]]
	binding_placeholders = '?, '*len(key)
	with sqlite3.connect(str(db_path)) as conn:
		conn.row_factory = sqlite3.Row
		query = f'''SELECT * from moz_places WHERE {key_type} IN ({binding_placeholders[:-2]})'''
		query_result = conn.execute(query, [*key])
		
		
		return query_result.fetchall()[:]


filepath_from_another = lambda filename, filepath=__file__: os.path.realpath(os.path.join(os.path.dirname(filepath), filename))


if __name__ == '__main__':
	from collections import OrderedDict as odict
	from pprint import pprint
	table = 'moz_places'
	fieldnames = ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
	              'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count',
	              'url_hash', 'description', 'preview_image_url',
	              ]
	queries = make_queries(table=table, fieldnames=', '.join(fieldnames))
	print(queries)
	keys_dict = {'id': (6, 10),
	             'guid': ('RcfYRk__x5kh', 'GfWa8wchW59X'),
	             'url_hash': (268504983346218, 47356520479868),
	             }
	for key_type, key_ in keys_dict.items():
		retrieved_records = retrieve_record('all_merged.sqlite', key=key_, key_type=key_type)
		for record in retrieved_records:
			pprint(odict(record))
