import sqlite3
import os

import read_browser_db
from db_handler import _db_tables

def quick_read_record(database):
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	print(_db_tables(cur))
	query = '''SELECT * FROM {}'''.format('moz_places')
	cur.execute(query)
	for record in cur:
		print(record)
		
# quick_read_record(database='test.sqlite')


def read_record_with_hash(database, url_hash):
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	query = '''SELECT * FROM {} where url_hash = ?'''.format('moz_places')
	cur.execute(query, url_hash)
	for record in cur:
		print(record)


if __name__ == '__main__':
	
	print(__file__)
	print(os.path.dirname(__file__))
	# quick_read_record(database='test.sqlite')
	
	# query = "SELECT name FROM sqlite_master WHERE type = 'table'"
	
	# read_record_with_hash(database='test.sqlite', url_hash=125511601170569)
	
	
	# conn = sqlite3.connect('test.sqlite')
	# cur = conn.cursor()
	#
	# query = "SELECT name FROM sqlite_master WHERE type = 'table'"
	# for table_ in cur.execute(query):
	# 	print(table_)

	# print(cur.fetchall())
	# for entry in cur:
	# 	print(entry)


'''
file_paths = read_browser_db.firefox()
prepped_records = read_browser_db.read_browser_db(filepaths=file_paths)  # gives a generator that yields all the records across all profiles.
# for profile_count, data_in_profile in enumerate(prepped_records):
# 	print('\n' * 2)
# 	print('profile count:', profile_count)
#
# 	for record_count, record in enumerate(data_in_profile ):
# 		print('record_count', record_count)
# 		print(record)
# 		record = deduplicator.deduplicate_records(record)
# 		print(record)
#
# 		input('next record')

'''
