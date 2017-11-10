import datetime
import json
import re
import sqlite3

from collections import namedtuple

from united_states_of_browsers.db_merge import database_operations as db_ops
from united_states_of_browsers.db_merge import helpers

from united_states_of_browsers.db_merge.paths_setup import app_inf_path
from united_states_of_browsers.db_merge.imported_annotations import *

from pprint import pprint


def build_search_table(db_path: PathInfo, included_fieldnames: Sequence[Text]):
	""" Builds virtual table for full-text search in sqlite databases.
	Accepts path to the sqlite file and subset of its fieldnames to be included in the virtual table.
	"""
	with sqlite3.connect(db_path) as sink_conn:
		column_str = ', '.join(included_fieldnames)
		create_table_query = f'''CREATE VIRTUAL TABLE search_table USING fts5({column_str});'''
		try:
			sink_conn.execute(create_table_query)
		except sqlite3.OperationalError as excep:
			print(f'{excep} Exception raised during '
			      f'sink_conn.execute({create_table_query}) '
			      f'in db_search.build_search_table()'
			      )
		sql_placeholder = ('?, ' * len(included_fieldnames))[:-2]
		record_yielder = db_ops.yield_source_records(source_db_paths={'all_merged': db_path},
		                                             source_fieldnames=included_fieldnames,
		                                             )
		virtual_insert_query = f'''INSERT INTO search_table ({column_str}) VALUES ({sql_placeholder})'''
		sink_conn.executemany(virtual_insert_query, tuple(record_yielder))


def _make_sql_statement(word_query: Text,
                        date_start: Union[int, None],
                        date_stop: Union[int, None]
                        ) -> Union[Text, Iterable[Text]]:
	""" Returns prepared SQL statements and bindings for queries with and without dates.
	Accepts word_query.
		Optional: date_start and date_stop.
	"""
	if date_start and date_stop:
		query_addon = ' AND last_visit_date BETWEEN ? AND ?'
		query_bindings = [word_query, date_start, date_stop]
	else:
		query_addon = ''
		query_bindings = [word_query]
	sql_query = ('SELECT * FROM moz_places'
	             ' WHERE id IN'
	             ' (SELECT id'
	             ' FROM search_table'
	             ' WHERE search_table'
	             f' MATCH ? ORDER BY bm25(search_table, 0, 7, 9, 0, 0, 0, 10)){query_addon}'
	             )
	return sql_query, query_bindings


def _run_search(db_path: PathInfo, sql_query: Text, query_bindings: Iterable[Text]
                ) -> Iterable[NamedTuple]:
	with open(app_inf_path, 'r') as read_json_obj:
		app_inf = json.load(read_json_obj)
	DBRecord = namedtuple('DBRecord', app_inf['source_fieldnames'])
	with sqlite3.connect(db_path) as sink_conn:
		sink_conn.row_factory = sqlite3.Row
		query_results = sink_conn.execute(sql_query, query_bindings)
		return [DBRecord(*result) for result in query_results]


def _print_search(search_results: Iterable):
	for result in search_results:
		timestamp_ = result.last_visit_date
		try:
			human_readable_date = datetime.datetime.utcfromtimestamp(timestamp_ / 10 ** 6)
		except TypeError as excep:
			human_readable_date = 'Date Unavailable'
		if not result.title:
			print(human_readable_date, '.', result.url)
		else:
			print(human_readable_date, '.', result.title)


def search(db_path, word_query, date_start=None, date_stop=None):
	helpers.query_sanitizer(word_query, exceptions=[' ', '%'])
	sql_query, query_bindings = _make_sql_statement(word_query, date_start, date_stop)
	search_results = _run_search(db_path, sql_query, query_bindings)
	return search_results


def parse_keywords(query):
	print(query)
	parsing = re.search("*\(*\)*", query)
	try:
		print(parsing.start(), parsing.end())
	except AttributeError:
		pass


if __name__ == '__main__':
	def _test_archive ():
		db_for_testing = db_test
		time_stamps = (1509123590555000, 1501259124168000, 1506703039399000)
		human_times = [datetime.datetime.utcfromtimestamp(timestamp_ / 10 ** 6) for timestamp_ in
		               time_stamps]
		
		search_test_cases = (
			(app_inf['sink'], 'python', time_stamps[1], time_stamps[2]),
			(app_inf['sink'], "python AND variable NOT update anaconda AND stackoverflow", None,
			 None),
			)
		
		for (db_path, word_query, date_start, date_stop) in search_test_cases:
			search_results = search(db_path, word_query, date_start, date_stop)
			_print_search(search_results)
			print()
		
		queries = ['india AND economy',
		           'javascript AND economy',
		           'javascript python NOT react']
		
		for query in queries[2:]:
			helpers.query_sanitizer(query)
			search_result = search(db_test, query)
			print(f'\nquery: {query}')
			pprint((search_result))
	
	
	root = Path(__file__).parents[2]
	db_test = str(root.joinpath('tests\\data\\db_for_testing_search.sqlite'))
	db_main = str(root.joinpath('db_merge\\all_merged.sqlite'))
	with open('app_inf.json', 'r') as json_obj:
		app_inf = json.load(json_obj)
	
	
	def _test(queries):
		for query in queries:
			helpers.query_sanitizer(query)
			search_result = search(db_test, query)
			print(f'\nquery: {query}')
			pprint((search_result))
	
	queries = ['python game NOT javascript',
	           ]
	
	_test(queries=queries)
