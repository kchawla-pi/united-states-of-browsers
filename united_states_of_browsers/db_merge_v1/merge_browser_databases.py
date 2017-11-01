# -*- encoding: utf-8 -*-
"""
python: 3.6
United States of Browsers aims to combine browser histories across different browsers and browser
profile to create one unified, searchable database.
Currently supports firefox profiles on Windows 10 x64.
Branch: Nightly-Dev
"""
import os

from united_states_of_browsers.db_merge_v1 import (db_handler,
                                                   read_browser_db,
                                                   write_new_db,
                                                   )
from united_states_of_browsers.db_merge_v1.imported_annotations import *


def write_url_hash_log(filename: Text, hashes: Sequence[int]):
	filemodes = {True: 'ab', False: 'wb'}
	try:
		filemode_ = filemodes[os.path.exists(filename)]
	except UnboundLocalError:
		print(f'At least one of the profiles seems to have no data to read.')
	else:
		with open(filename, filemode_) as write_obj:
			write_obj.write(hashes)


def merge(output_db: Optional[Text]= None,
          profiles: Optional[Union[Text, Iterable[Text]]]=None,
          show_records: Union[bool, int] = False
          ):
	source_db_paths, field_names = read_browser_db.firefox(profiles=profiles)
	prepped_records = read_browser_db.read_browser_database(filepaths=source_db_paths, fieldnames=field_names)
	yield_source_records = (record for profile_ in prepped_records for record in profile_)
		# yield_source_records: a generator that yields all the records across all profiles.
	
	try:
		sink_db_path, url_hash_log_file = write_new_db.setup_output_db_paths(output_db)
	except AttributeError:  # when output_db == None
		sink_db_info = None  # when None, merged records are returned, not written to DB.
	else:
		sink_db_info = db_handler.connect_db(db_file=sink_db_path)
		
	url_hashes, all_records = write_new_db.merge_databases(source_record_yielder=yield_source_records,
	                                                       sink_db_info=sink_db_info,
	                                                       show_records=show_records
	                                                       )
	if sink_db_info:
		write_url_hash_log(filename=url_hash_log_file, hashes=url_hashes)
	
	return url_hashes, all_records


if __name__ == '__main__':
	ask = input('Run database merge_records operation?\n'
	            'Press <n> to abort, <ENTER> for viewing the merged reuslts without writing it to a new database file.\n'
	            'Type a filename write the merged results to a database file.')
	if ask.lower() == 'n':
		print('Program terminated.')
		os.sys.exit()
	elif not ask:
		from pprint import pprint
		pprint(merge(output_db=None))
	elif ask:
		merge(output_db=f'{ask}.sqlite')


'''
python -m united_states_of_browsers.db_merge_v1.__main__
python united_states_of_browsers\db_merge_v1\__main__.py
'''
