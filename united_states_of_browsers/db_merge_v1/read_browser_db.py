# -*- encoding: utf-8 -*-
import sqlite3

from collections import OrderedDict as odict

from united_states_of_browsers.db_merge_v1 import browser_setup
from united_states_of_browsers.db_merge_v1 import db_handler
from united_states_of_browsers.db_merge_v1 import helpers
from united_states_of_browsers.db_merge_v1 import record_fetcher

from united_states_of_browsers.db_merge_v1.imported_annotations import *


def firefox(profiles: Optional[Union[Text, Sequence[Text]]]=None) -> Tuple[List[PathInfo], List[Text]]:
	'''
	Setups path & field names of places.sqlite file for Firefox browser profiles in Windows x64.
	Returns all profiles by default.
	Optionally, Accepts profile name or list of profile names.
	Returns tuple of list of Paths and field_names
	'''
	firefox_fieldnames = ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
	                       'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count',
	                       'url_hash', 'description', 'preview_image_url',
	                       ]
	profile_paths = browser_setup.setup_profile_paths(browser_ref='firefox', profiles=profiles)
	file_paths = browser_setup.db_filepath(profile_paths=profile_paths, filenames='places', ext='sqlite')
	return file_paths, firefox_fieldnames


def make_record_dict_template(cursor: sqlite3.Connection.cursor, table: Union[str, Sequence[str]]) -> [Dict, Exception] :
	'''
	Retrieves fieldnames from database table.
	Returns Ordered dictionary with field names as keys and None values.
	args: connection.cursor(), table name (str)
	'''
	helpers.safetychecks(table)  # Guards against SQL injection attacks
	query = '''SELECT * FROM {}'''.format(table)
	try:
		cursor.execute(query)
	except sqlite3.OperationalError:
		return Exception(table)
	field_names = [desc_[0] for desc_ in cursor.description]
	record_template = odict.fromkeys(field_names, None)
	return record_template
	
	
def read_browser_database(filepaths: Union[Text, Sequence[Text]], fieldnames: Sequence[Text]) -> Generator:
	'''
	Yields a generator of generator of records from all the profile databases.
	Accepts a single path or a sequence of paths to each database file, and list of field names of records.
	'''
	record_template = odict.fromkeys(fieldnames, None)
	helpers.safetychecks(record_template)  # Checks fieldnames to prevent SQL injection attacks.
	for idx, profile_name_ in enumerate(filepaths):
		tables = ['moz_places']
		for table_ in tables:
			try:
				source_db_info = db_handler.connect_db(db_file=filepaths[profile_name_])
			except sqlite3.OperationalError as excep:
				print(excep)
			else:
				prepped_records = record_fetcher.yield_prepped_records(cursor=source_db_info['cursor'],
				                                                       table=table_,
				                                                       record_template=record_template,
				                                                       )
				yield prepped_records  # generator that yields DB records.
			finally:
				source_db_info['cursor'].close()
				source_db_info['connection'].close()


def chrome():
	home_dir = Path.home()
	file_paths = browser_setup.db_filepath(
				root=f'{home_dir}\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
				filenames='History', ext=None)
	

if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	# firefox(['test_profile0'])
	filepaths = firefox('default')
	yield_db = read_browser_database(filepaths)
	for rec in yield_db:
		for entry in rec:
			print(entry)
