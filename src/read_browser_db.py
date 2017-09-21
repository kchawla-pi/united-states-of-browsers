import sqlite3

import db_handler
import record_fetcher
import browser_setup


def firefox(profiles=None):
	profile_paths = browser_setup.setup_profile_paths(browser_name_or_path='firefox',
	                                                  profiles=profiles)
	file_paths = browser_setup.db_filepath(root=profile_paths, filenames='places', ext='sqlite')
	for idx, file_ in enumerate(file_paths):
		# print('\n', '=' * 50, '\n')
		# conn, cur, filename = db_handler.connect_db(db_file=file_)
		# tables = _db_tables(cursor=cur)
		tables = ['moz_places']
		for table_ in tables:
			# print('.' * 8)
			try:
				conn, cur, filename = db_handler.connect_db(db_file=file_)
			except sqlite3.OperationalError as excep:
				print(excep)
			else:
				prepped_records = (
					record_fetcher.yield_prepped_records(cursor=cur, table=table_, filepath=file_))
				for record in prepped_records:
					print(record)
					quitter = input()
					if quitter:
						break
				# if prepped_records:
				# 	print(profiles, len(prepped_records))
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
