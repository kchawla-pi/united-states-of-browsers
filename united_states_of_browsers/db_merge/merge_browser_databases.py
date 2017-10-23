# -*- encoding: utf-8 -*-
"""
python: 3.6
United States of Browsers aims to combine browser histories across different browsers and browser
profile to create one unified, searchable database.
Currently supports firefox profiles on Windows 10 x64.
Branch: Nightly-Dev
"""
import os

from united_states_of_browsers.db_merge import db_handler
from united_states_of_browsers.db_merge import helpers
from united_states_of_browsers.db_merge import read_browser_db
from united_states_of_browsers.db_merge import write_new_db
from united_states_of_browsers.db_merge.imported_annotations import *


def merge(output_db: [Text, bool],
          output_ext: Text='sqlite',
          profiles: Optional[Union[Text, Iterable[Text]]]=None,
          ):
	source_db_paths, field_names = read_browser_db.firefox(profiles=profiles)
	
	prepped_records = read_browser_db.read_browser_database(filepaths=source_db_paths, fieldnames=field_names)
	# gives a generator that yields all the records across all profiles.
	yield_source_records = (record for profile_ in prepped_records for record in profile_)
	
	try:
		output_db, output_ext = output_db.split(os.extsep)
	except ValueError:
		output_db = output_db
		
	ext_sep = '' if output_ext[0] in {'.', os.extsep} else os.extsep
	sink_db_path = helpers.filepath_from_another(ext_sep.join([output_db, output_ext]))
	
	url_hash_log_filename = '_'.join([os.path.splitext(output_db)[0], 'url_hash_log.bin'])
	url_hash_log_file = helpers.filepath_from_another(url_hash_log_filename)
	
	# target database connection object
	if output_db:
		sink_db_info = db_handler.connect_db(db_file=sink_db_path)
	else:
		sink_db_info = False
	url_hashes, all_records = write_new_db.merge_databases(source_record_yielder=yield_source_records,
	                                                       sink_db_info=sink_db_info,
	                                                       show_records=4000
	                                                       )
	if all_records:
		return url_hashes, all_records
	else:
		filemodes = {True: 'ab', False: 'wb'}
		filemode_ = filemodes[os.path.exists(url_hash_log_file)]
		with open(url_hash_log_file, filemode_) as write_obj:
			write_obj.write(url_hashes)
		return None, None


if __name__ == '__main__':
	ask = input('Run database merge operation?(y/n)')
	if ask.lower() == 'y':
		merge(output_db='merged_fx_db.sqlite')
	else:
		print('Program terminated.')


'''
python -m united_states_of_browsers.db_merge.__main__
python united_states_of_browsers\db_merge\__main__.py
'''
