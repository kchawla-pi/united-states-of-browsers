import json
import sqlite3

from pprint import pprint

from united_states_of_browsers.db_merge import database_operations as db_ops


def build_search_table(db_path, included_fieldnames):
	
	with sqlite3.connect(db_path) as sink_conn:
		column_str = ', '.join(included_fieldnames)
		create_table_query = f'''CREATE VIRTUAL TABLE history USING fts5({column_str});'''
		try:
			sink_conn.execute(create_table_query)
		except sqlite3.OperationalError:
			pass
	
	record_yielder = db_ops.yield_source_records(source_db_paths={'all_merged': db_path},
	                                      source_fieldnames=included_fieldnames,
	                                      )
	virtual_insert_query = f'''INSERT INTO history {included_fieldnames} VALUES (?, ?, ?, ?, ?, ?)'''
	sink_conn.executemany(virtual_insert_query, tuple(record_yielder))
	

def create_search_query(query_and, query_or=None, query_not=None):
	pass


def run_search(path_info, search_query):
	# path_info.get(
	with sqlite3.connect(path_info['sink']) as sink_conn:
		search_query = sink_conn.execute(
				"""SELECT * FROM history WHERE history MATCH
				'title:python AND list AND pep NOT machine';"""
				)
		for result in search_query:
			print(result)
	
with open('path_info.json', 'r') as json_obj:
	path_info = json.load(json_obj)
included_fieldnames = ('url', 'title', 'visit_count', 'last_visit_date', 'url_hash', 'description')
build_search_table(db_path=path_info['sink'], included_fieldnames=included_fieldnames)
