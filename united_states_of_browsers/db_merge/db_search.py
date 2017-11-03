import datetime
import json
import re
import sqlite3
from collections import (namedtuple,
                         )

from united_states_of_browsers.db_merge import database_operations as db_ops
from united_states_of_browsers.db_merge.paths_setup import app_inf_path
from united_states_of_browsers.db_merge.imported_annotations import *


search_table_fieldnames = ('id', 'url', 'title', 'visit_count',
                           'last_visit_date', 'url_hash', 'description')

with open(app_inf_path, 'r') as json_obj:
	app_inf = json.load(json_obj)

# SearchRecord = namedtuple('SearchRecord', app_inf['search_table_fields'])
DBRecord = namedtuple('DBRecord', app_inf['source_fieldnames'])

def build_search_table(db_path: PathInfo, included_fieldnames: Sequence[Text]):
	""" Builds virtual table for full-text search in sqlite databases.
	Accepts path to the sqlite file and subset of its fieldnames to be included in the virtual table.
	
	db_path: Path to the SQLite Database file. (str, bytestring, Path, PathLike)
	included_fieldnames: Ordered subset of the database's fieldnames to be included in the search table.
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


def parse_search_query(query):
	print(query)
	parsing = re.search("*\(*\)*", query)
	try:
		print(parsing.start(), parsing.end())
	except AttributeError:
		pass


def create_search_query(any_word, all_words=None, not_words=None):
	words_any = ' OR '.join(any_word)
	words_all = ' AND '.join(all_words)
	words_not = ' NOT '.join(not_words)
	return words_any, words_all, words_not


# print(repr(words_any))
# print(repr(words_all))
# print(repr(words_not))


def run_search(db_path, search_query):
	# db_path.get(
	with sqlite3.connect(db_path) as sink_conn:
		query_results = sink_conn.execute(
				"""SELECT *
				FROM search_table
				WHERE search_table
				MATCH ?""", [search_query]
				)
		for result in query_results:
			print(result)


def run_search_long(db_path, word_query, date_start=None, date_stop=None):
	# db_path.get(
	sql_query = ('SELECT *'
	             ' FROM moz_places'
	             ' WHERE id IN'
	             ' (SELECT id'
	             ' FROM search_table'
	             ' WHERE search_table'
	             ' MATCH ?)'
	             ' AND last_visit_date'
	             ' BETWEEN ? AND ?')
	# pp = pprint.PrettyPrinter(indent=4, compact=False)
	with sqlite3.connect(db_path) as sink_conn:
		sink_conn.row_factory = sqlite3.Row
		query_results = sink_conn.execute(sql_query, [word_query, date_start, date_stop])
		for result in query_results:
			search_record = DBRecord(*result)
			timestamp_ = search_record.last_visit_date
			human_readable_date = datetime.datetime.utcfromtimestamp(timestamp_ / 10 ** 6)
			# pp.pprint(DBRecord(*result).title)
			print(human_readable_date, '.', search_record.title)
			# pprint([human_readable_date, search_record.title, search_record.url])
			# pprint(DBRecord(*result))
	


def build_new_search_table():
	with open('app_inf.json', 'r') as json_obj:
		app_inf = json.load(json_obj)
	# included_fieldnames = (
	# 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash', 'description')
	build_search_table(db_path=app_inf['sink'], included_fieldnames=app_inf['search_table_fields'])


if __name__ == '__main__':
	time_stamps = (1509123590555000, 1501259124168000, 1506703039399000)
	human_times = [datetime.datetime.utcfromtimestamp(timestamp_ / 10 ** 6) for timestamp_ in
	               time_stamps]
	
	# pprint(human_times[1:])
	# run_search_long(db_path=app_inf['sink'], word_query='python', date_start=time_stamps[1],
	#                 date_stop=time_stamps[2])
	# pprint(human_times[1:])
	
	run_search_long(db_path=app_inf['sink'], word_query='python', date_start=time_stamps[1])
	"""
	entered_searches, search_queries = get_searches_list()
	for query in entered_searches:
		pass
	# parse_search_query(query=query)
	
	
	search_query = create_search_query(any_word=['python', 'pep', 'list'],
	                                   all_words=['machine', 'learning'],
	                                   not_words=['numpy', 'javascript']
	                                   )
	
	# pprint(app_inf)
	# search_query = 'title:python'
	
	search_query = "python AND variable NOT update anaconda AND stackoverflow"
	run_search(db_path=app_inf['sink'], search_query=search_query)
	# print(datetime.datetime.utcfromtimestamp(1509123590555000/10**6))
	# run_search_long(path_info=app_inf['sink'], word_query='python', )
	"""
