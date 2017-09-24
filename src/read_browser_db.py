import sqlite3

import browser_setup
import db_handler
import record_fetcher
import reorganizer

def print_records(record_gen, each_time=10, profile_name=None):
	import time
	if profile_name:
		print('\n' * 2, profile_name, '\n' * 2)
	time.sleep(2)
	print('Press ENTER key for the next set of records, c for number of records so far, any other to exit.\n\n')
	time.sleep(1)
	for srn, record in enumerate(record_gen):
		print(record)
		try:
			cond = srn % each_time == 0 and srn > 0
		except TypeError:
			pass
		else:
			if cond:
				quitter = input()
				if quitter in {'c', 'C'}:
					print(srn)
					time.sleep(1)
				elif quitter:
					break
				pass
				
	
def firefox(profiles=None):
	profile_paths = browser_setup.setup_profile_paths(browser_ref='firefox',
	                                                  profiles=profiles)
	file_paths = browser_setup.db_filepath(profile_paths=profile_paths, filenames='places', ext='sqlite')
	for idx, profile_name_ in enumerate(file_paths):
		tables = ['moz_places']
		for table_ in tables:
			try:
				conn, cur, filename = db_handler.connect_db(db_file=file_paths[profile_name_])
			except sqlite3.OperationalError as excep:
				print(excep)
			else:
				prepped_records = record_fetcher.yield_prepped_records(cursor=cur, table=table_,
				                                                       filepath=file_paths[profile_name_])
				# yield prepped_records
				print_records(record_gen=prepped_records, each_time='all', profile_name=profile_name_)
				# all_url_hashes = reorganizer.deduplicate_sites(prepped_records)
				# print(len(all_url_hashes))
			finally:
				cur.close()
				conn.close()


def chrome():
	file_paths = browser_setup.db_filepath(
				root="C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
				filenames='History', ext=None)
	


if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	firefox()
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
