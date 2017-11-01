import json
import sqlite3

from pprint import pprint

from united_states_of_browsers.db_merge import merge_browser_databases as mbdb

with open('path_info.json', 'r') as json_obj:
	path_info = json.load(json_obj)
	

print(path_info['sink'])

with sqlite3.connect(path_info['sink']) as sink_conn:
	print(sink_conn)
	try:
		sink_conn.execute("""DROP TABLE history""")
	except sqlite3.OperationalError:
		sink_conn.execute(
				'''CREATE VIRTUAL TABLE history
				USING fts5(url, title, url_hash, description, visit_count, last_visit_date);'''
				)
	source_fieldnames = ('url', 'title', 'visit_count', 'last_visit_date', 'url_hash', 'description')
	
	record_yielder = mbdb.yield_source_records(source_db_paths={'all_merged': path_info['sink']},
	                                            source_fieldnames =source_fieldnames,
	                                            )
	for rec in record_yielder:
		print(rec)
	# sink_conn.executemany(f'''INSERT INTO history {source_fieldnames} VALUES (?, ?, ?, ?, ?, ?)''', record_yielder)
	quit()
	
	
	
	sink_conn.execute("""DROP TABLE history""")
	try:
		search_query = sink_conn.execute("""SELECT * FROM history WHERE history MATCH 'url:www'""")
	except sqlite3.OperationalError:
		sink_conn.execute(
				'''CREATE VIRTUAL TABLE history
				USING fts5(url, title, url_hash, description, visit_count, last_visit_date);'''
				)
		print('+++')
		search_query = sink_conn.execute("""SELECT * FROM history WHERE history MATCH 'url:www'""")
	
	for result in search_query:
		print(result)
		print('...')
	print('***')
