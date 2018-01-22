from collections import namedtuple
from typing import Text, Sequence, Dict, Union, Iterable


def make_queries(tablename: Text, fieldnames: Sequence[Text]) -> Dict:
	""" Constructs the queries necessary for specific purposes.
	Returns them as dict['purpose': 'query']
	"""
	filednames_str = ', '.join(fieldnames)
	query_placeholder = '?, ' * len(fieldnames)
	queries = {'create': f'''CREATE TABLE {tablename} ({filednames_str[:]})'''}
	queries.update({'insert': f"INSERT INTO {tablename} VALUES ({query_placeholder[:-2]})"})
	return queries


def query_sanitizer(query: str, allowed_chars: Union[str, Iterable]='_') -> str:
	""" Removes non-alphanumeric characters from a query.
	Retains characters passed in via `allowed_chars`. (Default: '_')
	Returns a string.
	"""
	allowed_chars = set(allowed_chars)
	return ''.join([char for char in query if char.isalnum() or char in allowed_chars])  #, '?', '(', ')', ','}])


def define_not_null_fields(table_obj):
	BrowserFileTableFields = namedtuple('BrowserFileTable', 'browser file tablename')
	not_null_fields_info = {
		BrowserFileTableFields(browser='firefox', file='places.sqlite', table='moz_places'): ('title', 'last_visit_date'),
		BrowserFileTableFields(browser='chrome', file='history', table='urls'): ('title', 'last_visit_time'),
		}
	query = BrowserFileTableFields(table_obj['browser'], table_obj['file'], table_obj['table'])
	return not_null_fields_info[query]
