import sqlite3

import browser_setup
import db_handler
import record_fetcher
import write_new_db


def quick_read_record(database):
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	query = '''SELECT * FROM {}'''.format('moz_places')
	cur.execute(query)
	for record in cur:
		print(record)

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
			
			
def test_print_records(cursor, table, prepped_records):
	for num1, record in enumerate(prepped_records):
		query = '''SELECT * FROM {}'''.format('moz_places')
		cursor.execute(query)
		for num2, record__ in enumerate(cursor):
			if num2 == 37:
				print(num2)
				print(record__)
				break
		
		print('-')
		if num1 == 37:
			print(num1)
			write_new_db.write_to_db(database='test.sqlite', record=record, table=table)
			print('wriiten')
			break
			
	
def firefox(profiles=None):
	profile_paths = browser_setup.setup_profile_paths(browser_ref='firefox', profiles=profiles)
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
				                                                       filepath=file_paths[profile_name_]
				                                                       )
				# for num1, record in enumerate(prepped_records):
				# 	write_new_db.write_to_db(record=record, table=table_)
				print_records(prepped_records)
				# test_print_records(cursor=cur, table=table_, prepped_records=prepped_records)

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
	firefox()
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
