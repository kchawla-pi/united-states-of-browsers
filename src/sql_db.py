import sqlite3
import os
from pprint import pprint

import browser_setup
import record_fetcher


def _connect_db(db_file):
	"""
	Establishes connection to the database file, returns connection, cursor objects and filename.
	:param db_file: Path of the database file.
	:type db_file: str/path-like object
	:return: conn, cur filename
	:rtype: connection object, cursor object, str
	"""
	# if not os.path.exists(db_file):
	#     print("ERROR: Invalid path. ({})".format(db_file))
	#     print("Quitting...")
	#     quit()
	conn = sqlite3.connect(database=db_file)
	cur = conn.cursor()
	return conn, cur, os.path.split(db_file)[1]


def _db_tables(cursor):
	"""
	Returns names of tables from the cursor object of the database file.
	:param cursor: Cursor object attached to the database file, from _connect_db function.
	:type cursor: Connection.Cursor Object
	:return: list of table names in database file.
	:rtype: list['str']
	"""
	query = "SELECT name FROM sqlite_master WHERE type = 'table'"
	return [table_[0] for table_ in cursor.execute(query)]


def firefox(profiles=None):
	# profile_paths = browser_setup.setup_profile_paths(browser_name_or_path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing')
	# profile_paths = browser_setup.setup_profile_paths(browser_name_or_path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
	profile_paths = browser_setup.setup_profile_paths(browser_name_or_path='firefox',
	                                                  profiles=profiles)
	file_paths = browser_setup.db_filepath(root=profile_paths, filenames='places', ext='sqlite')
	for idx, file_ in enumerate(file_paths):
		# print('\n', '=' * 50, '\n')
		# conn, cur, filename = _connect_db(db_file=file_)
		# tables = _db_tables(cursor=cur)
		tables = ['moz_places']
		for table_ in tables:
			# print('.' * 8)
			try:
				conn, cur, filename = _connect_db(db_file=file_)
			except sqlite3.OperationalError:
				pass
			else:
				prepped_records = list(
					record_fetcher.yield_prepped_records(cursor=cur, table=table_, filepath=file_))
				if prepped_records:
					print(profiles, len(prepped_records))
			finally:
				cur.close()


def chrome():
	file_paths = browser_setup.db_filepath(
				root="C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
				filenames='History', ext=None)
	
	
	"C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"


if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	firefox('RegularSurfing')
	# chrome()
