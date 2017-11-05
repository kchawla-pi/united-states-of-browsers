import json
import random
import sqlite3

from collections import OrderedDict as odict

from collections import namedtuple
from pathlib import Path

# 'C:\Users\kshit\Dropbox\workspace\UnitedStatesOfBrowsers\united_states_of_browsers\tests\data'

DBRecord = []
SearchRecord = []

def setup_paths():
	root = Path(__file__).parents[2]
	src_db_path = Path.joinpath(root, 'united_states_of_browsers', 'db_merge', 'all_merged.sqlite')
	sink_db_path = Path.joinpath(root, 'tests', 'data', 'db_for_testing_search.sqlite')
	url_log_path = Path.joinpath(sink_db_path.parent,
	                             f'{sink_db_path.stem}_written_url_hashes.json')
	return src_db_path, sink_db_path, url_log_path
		
		
def get_fieldnames():
	firefox_fieldnames = ['id',
	                      'url',
	                      'title',
	                      'rev_host',
	                      'visit_count',
	                      'hidden',
	                      'typed',
	                      'favicon_id',
	                      'frecency',
	                      'last_visit_date',
	                      'guid',
	                      'foreign_count',
	                      'url_hash',
	                      'description',
	                      'preview_image_url',
	                      ]
	search_table_fieldnames = ["id",
	                           "url",
	                           "title",
	                           "visit_count",
	                           "last_visit_date",
	                           "url_hash",
	                           "description",
	                           ]
	global DBRecord, SearchRecord
	DBRecord = namedtuple('DBRecord', firefox_fieldnames)
	SearchRecord = namedtuple('SearchRecord', search_table_fieldnames)
 
	return firefox_fieldnames, search_table_fieldnames


def get_records_for_test_db(src_db_path, num_rec):
	with sqlite3.connect(str(src_db_path)) as src_conn:
		src_conn.row_factory = sqlite3.Row
		query_yield = src_conn.execute('''SELECT * FROM moz_places''')
		# all_records = [DBRecord(record) for record in enumerate(query_yield)]
		all_records = query_yield.fetchall()
	chosen_records = random.choices(all_records, k=num_rec)
	chosen_records = [DBRecord(*record) for record in chosen_records]
	return chosen_records


def make_test_db(sink_db_path, firefox_fieldnames, chosen_records):
	fx_fieldnames_str = ', '.join(firefox_fieldnames)
	with sqlite3.connect(str(sink_db_path)) as sink_conn:
		try:
			sink_conn.execute(f'''CREATE TABLE moz_places ({fx_fieldnames_str})''')
		except sqlite3.OperationalError as excep:
			print(excep.args)
		sink_conn.executemany(f'''INSERT INTO moz_places VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', chosen_records)
		url_hashes_query_result = sink_conn.execute('''SELECT id, url_hash FROM moz_places''')
		written_url_hashes = odict(url_hashes_query_result.fetchall())
	return written_url_hashes
	
	
def make_search_table(sink_db_path, search_table_fieldnames, search_records_yielder):
	fx_incl_fieldnames_str = ', '.join(search_table_fieldnames)
	with sqlite3.connect(str(sink_db_path)) as sink_conn:
		try:
			sink_conn.execute(f'''CREATE VIRTUAL TABLE search_table USING fts5({fx_incl_fieldnames_str});''')
		except sqlite3.OperationalError as excep:
			print(excep)
		search_insert_query = f'''INSERT INTO search_table ({fx_incl_fieldnames_str}) VALUES (?, ?, ?, ?, ?, ?, ?)'''
		sink_conn.executemany(search_insert_query, tuple(search_records_yielder))


def make_search_records(db_records):
	return (SearchRecord(*[record.__getattribute__(fieldname)
	                       for fieldname in SearchRecord._fields
	                       ]
	                     )
	        for record in db_records
	        )
	
def save_url_hashes(url_log_path, written_url_hashes):
	with open(str(url_log_path), 'w') as write_obj:
		json.dump(dict(written_url_hashes), write_obj, sort_keys=True,indent=4,)
	
def create_test_db(number_of_records):
	global DBRecords
	src_db_path, sink_db_path, url_log_path  = setup_paths()
	if sink_db_path.exists():
		print(f'{sink_db_path.name} already exists at \n{sink_db_path.parent}')
	else:
		firefox_fieldnames, search_table_fieldnames = get_fieldnames()
		chosen_records = get_records_for_test_db(src_db_path, num_rec=number_of_records)
		
		search_records_yielder = make_search_records(db_records=chosen_records)
		written_url_hashes  = make_test_db(sink_db_path, firefox_fieldnames, chosen_records)
		save_url_hashes(url_log_path, written_url_hashes)
		make_search_table(sink_db_path, search_table_fieldnames, search_records_yielder)


if __name__ == '__main__':
	create_test_db(100)
