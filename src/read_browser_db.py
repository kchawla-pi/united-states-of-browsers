import sqlite3

import browser_setup
import db_handler
import record_fetcher
import write_new_db
from show import quick_read_record


def firefox(profiles=None):
	'''
	Setups
	:param profiles:
	:type profiles:
	:return:
	:rtype:
	'''
	profile_paths = browser_setup.setup_profile_paths(browser_ref='firefox', profiles=profiles)
	file_paths = browser_setup.db_filepath(profile_paths=profile_paths, filenames='places', ext='sqlite')
	return file_paths

	
def read_browser_db(filepaths):
	for idx, profile_name_ in enumerate(filepaths):
		tables = ['moz_places']
		for table_ in tables:
			try:
				conn, cur, filename = db_handler.connect_db(db_file=filepaths[profile_name_])
			except sqlite3.OperationalError as excep:
				print(excep)
			else:
				prepped_records = record_fetcher.yield_prepped_records(cursor=cur, table=table_,
				                                                       filepath=filepaths[profile_name_]
				                                                       )
				yield prepped_records
				

			finally:
				cur.close()
				conn.close()


def chrome():
	file_paths = browser_setup.db_filepath(
				root="C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
				filenames='History', ext=None)
	

if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	# firefox(['test_profile0'])
	read_browser_db(firefox())
	quit()
	quick_read_record(database='test.sqlite')

# chrome()

"""
read db: done
process records bfeore adding: (pending)
 - remove duplicates ( hash in a set, membership tests from new db)
 - give new primary key
 - update last visited to latest among duplicates
 - update number of visits for duplicates
take record and add to new db: done
"""
