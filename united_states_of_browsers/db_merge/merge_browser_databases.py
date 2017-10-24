# -*- encoding: utf-8 -*-
"""
python: 3.6
United States of Browsers aims to combine browser histories across different browsers and browser
profile to create one unified, searchable database.
Currently supports firefox profiles on Windows 10 x64.
Branch: Nightly-Dev
"""
import os

from united_states_of_browsers.db_merge import (db_handler,
                                                helpers,
                                                read_browser_db,
                                                write_new_db,
                                                )
from united_states_of_browsers.db_merge.imported_annotations import *


def merge(output_db: Optional[Text]= None,
          profiles: Optional[Union[Text, Iterable[Text]]]=None,
          ):
	source_db_paths, field_names = read_browser_db.firefox(profiles=profiles)
	prepped_records = read_browser_db.read_browser_database(filepaths=source_db_paths, fieldnames=field_names)
	# gives a generator that yields all the records across all profiles.
	yield_source_records = (record for profile_ in prepped_records for record in profile_)
	
	
	if output_db:
		sink_db_path, url_hash_log_file = write_new_db.setup_output_db_paths(output_db)
		# target database connection object
		sink_db_info = db_handler.connect_db(db_file=sink_db_path)
	else:
		sink_db_info = None
	url_hashes, all_records = write_new_db.merge_databases(source_record_yielder=yield_source_records,
	                                                       sink_db_info=sink_db_info,
	                                                       show_records=4000
	                                                       )
	if all_records:
		return url_hashes, all_records
	else:
		filemodes = {True: 'ab', False: 'wb'}
		try:
			filemode_ = filemodes[os.path.exists(url_hash_log_file)]
		except UnboundLocalError as excep:
			print(f'Atleast one of the profiles seems to have no data to read.')
		else:
			with open(url_hash_log_file, filemode_) as write_obj:
				write_obj.write(url_hashes)
		return None, None


if __name__ == '__main__':
	ask = input('Run database merge operation?\n'
	            'Press <n> to abort, <ENTER> for uncommitted merge.\n'
	            'Type a filename for a committed merge.')
	if ask.lower() == 'n':
		print('Program terminated.')
		os.sys.exit()
	elif not ask:
		from pprint import pprint
		pprint(merge(output_db=None))
	elif ask:
		f'{ask}.sqlite'


'''
python -m united_states_of_browsers.db_merge.__main__
python united_states_of_browsers\db_merge\__main__.py
'''
