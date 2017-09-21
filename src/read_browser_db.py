import sqlite3

import db_handler
import record_fetcher
import browser_setup

def print_records(record_gen, each_time=10):
	import time
	print('Press ENTER key for the next set of records, c for number of records so far, any other to exit.\n\n')
	time.sleep(1)
	for srn, record in enumerate(record_gen):
		print(record)
		if srn % each_time == 0 and srn > 0:
			quitter = input()
			if quitter in {'c', 'C'}:
				print(srn)
				time.sleep(1)
			elif quitter:
				break
			pass
			
	
def firefox(profiles=None):
	profile_paths = browser_setup.setup_profile_paths(browser_name_or_path='firefox',
													  profiles=profiles)
	file_paths = browser_setup.db_filepath(root=profile_paths, filenames='places', ext='sqlite')
	for idx, file_ in enumerate(file_paths):
		tables = ['moz_places']
		for table_ in tables:
			try:
				conn, cur, filename = db_handler.connect_db(db_file=file_)
			except sqlite3.OperationalError as excep:
				print(excep)
			else:
				prepped_records = record_fetcher.yield_prepped_records(cursor=cur, table=table_,
				                                                       filepath=file_)
				print_records(record_gen=prepped_records, each_time=10)
			finally:
				cur.close()
				conn.close()


def chrome():
	file_paths = browser_setup.db_filepath(
				root="C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
				filenames='History', ext=None)
	
	"C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"


if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	firefox('RegularSurfing')
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
