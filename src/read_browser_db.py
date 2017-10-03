import sqlite3

from collections import OrderedDict as odict

import browser_setup
import db_handler
import helpers
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


def make_record_dict_template(cursor, table):
	helpers.safetychecks(table)
	query = '''SELECT * FROM {}'''.format(table)
	try:
		cursor.execute(query)
	except sqlite3.OperationalError:
		return Exception(table)
	field_names = [desc_[0] for desc_ in cursor.description]
	record_template = odict.fromkeys(field_names, None)
	return record_template
	
	
def read_browser_database(filepaths):
	fieldnames_template = ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
	                       'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count',
	                       'url_hash', 'description', 'preview_image_url',
	                       ]
	record_template = odict.fromkeys(fieldnames_template, None)
	for idx, profile_name_ in enumerate(filepaths):
		tables = ['moz_places']
		for table_ in tables:
			try:
				source_db_info = db_handler.connect_db(db_file=filepaths[profile_name_])
			except sqlite3.OperationalError as excep:
				print(excep)
			else:
				prepped_records = record_fetcher.yield_prepped_records(cursor=source_db_info['cursor'], table=table_,
				                                                       filepath=filepaths[profile_name_],
				                                                       record_template=record_template,
				                                                       )
				yield prepped_records
			finally:
				source_db_info['cursor'].close()
				source_db_info['connection'].close()


def chrome():
	file_paths = browser_setup.db_filepath(
				root="C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
				filenames='History', ext=None)
	

if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	# firefox(['test_profile0'])
	filepaths = firefox('default')
	yield_db = read_browser_database(filepaths)
	for rec in yield_db:
		for entry in rec:
			print(entry)
	# read_browser_database({'default': 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xl8257ca.default\\places.sqlite'})
	# quit()
	# quick_read_record(database='test.sqlite')

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
