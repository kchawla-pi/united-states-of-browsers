import json
import random
import sqlite3

from collections import OrderedDict as odict
from pprint import pprint

from collections import namedtuple
from pathlib import Path

# 'C:\Users\kshit\Dropbox\workspace\UnitedStatesOfBrowsers\united_states_of_browsers\tests_unfinished\data'

DBRecord = []
SearchRecord = []

def setup_paths():
	root = Path(__file__).parents[2]
	src_db_path = root.joinpath('united_states_of_browsers', 'AppData', 'all_merged.sqlite')
	sink_db_path = root.joinpath('tests_unfinished', 'data', 'db_for_testing_search.sqlite')
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
	                           "guid",
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
	
	
def make_search_table(sink_db_path, search_table_fieldnames, search_records_yielder=None):
	fx_incl_fieldnames_str = ', '.join(search_table_fieldnames)
	query_bindings_placeholder = '?, ' * len(search_table_fieldnames)
	with sqlite3.connect(str(sink_db_path)) as sink_conn:
		try:
			sink_conn.execute(f'''CREATE VIRTUAL TABLE search_table USING fts5({fx_incl_fieldnames_str});''')
		except sqlite3.OperationalError as excep:
			print(excep)
		if not search_records_yielder:
			search_records_yielder = sink_conn.execute(f"SELECT {fx_incl_fieldnames_str} FROM moz_places")
			search_records_yielder.row_factory = sqlite3.Row
		search_insert_query = f'''INSERT INTO search_table ({fx_incl_fieldnames_str}) VALUES ({query_bindings_placeholder[:-2]})'''
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
	src_db_path, sink_db_path, url_log_path = setup_paths()
	if sink_db_path.exists():
		print(f'{sink_db_path.name} already exists at \n{sink_db_path.parent}')
	else:
		firefox_fieldnames, search_table_fieldnames = get_fieldnames()
		chosen_records = get_records_for_test_db(src_db_path, num_rec=number_of_records)
		
		search_records_yielder = make_search_records(db_records=chosen_records)
		written_url_hashes  = make_test_db(sink_db_path, firefox_fieldnames, chosen_records)
		save_url_hashes(url_log_path, written_url_hashes)
		make_search_table(sink_db_path, search_table_fieldnames, search_records_yielder)


def retrieve_record_using_id(primary_key):
	_, search_db_path, _ = setup_paths()
	with sqlite3.connect(str(search_db_path)) as conn:
		conn.row_factory = sqlite3.Row
		query = f'''SELECT * from moz_places WHERE id is ?'''
		query_result = conn.execute(query, [primary_key])
		return query_result.fetchall()[:]


def recreate_search_table():
	_, search_table_fieldnames = get_fieldnames()
	# with sqlite3.connect('db_for_testing_search.sqlite') as conn:
	# 	all_records = conn.execute("SELECT * FROM moz_places")
	# 	conn.row_factory = sqlite3.Row
	make_search_table('db_for_testing_search.sqlite', search_table_fieldnames)


def log_guids_file():
	with sqlite3.connect('db_for_testing_search.sqlite') as conn:
		query = conn.execute("SELECT guid FROM moz_places")
		all_guids = query.fetchall()
	guids = [guid_[0] for guid_ in all_guids]
	with open('test_db_guids.txt', 'w') as write_guids:
		write_guids.write(', '.join(guids))

def edit_table():
	from datetime import datetime as dt
	from collections import OrderedDict as odict
	moz_places_fields = ('id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id', 'frecency',
	                     'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description', 'preview_image_url',
	                     'last_visit_date_readable'
	                     )
	bindings_placeholders = '?, ' * len(moz_places_fields)
	with sqlite3.connect('db_for_testing_search.sqlite') as source_conn:
		source_conn.row_factory = sqlite3.Row
		query_source_result = source_conn.execute('SELECT * FROM moz_places')
		with sqlite3.connect('db_for_testing_search_new.sqlite') as sink_conn:
			try:
				query_sink_result = sink_conn.execute(f"CREATE TABLE moz_places ({', '.join(moz_places_fields)})")
			except Exception as excep:
				print(excep)
			finally:
				for row in query_source_result :
					row = odict(row)
					row.setdefault('last_visit_date_readable', None)
					try:
						row['last_visit_date_readable'] = dt.fromtimestamp(row['last_visit_date'] // 10**6).strftime('%x %X')
					except TypeError:
						pass
					sink_conn.execute(f'INSERT INTO moz_places VALUES ({bindings_placeholders[:-2]})', row)

if __name__ == '__main__':
	# create_test_db(100)
	edit_table()
	# recreate_search_table()

# selected_primary_keys = [7787]
	# for primary_key in selected_primary_keys:
	# 	print(retrieve_record_using_id(primary_key), end='\n')
