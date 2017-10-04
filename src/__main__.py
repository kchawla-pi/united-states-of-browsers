# -*- encoding: utf-8 -*-
"""
python: 3.6
United States of Browsers aims to combine browser histories across different browsers and browser
profile to create one unified, searchable database.
Currently supports firefox profiles on Windows 10 x64.
Branch: Nightly-Dev
"""
import os

import db_handler
import helpers
import read_browser_db
import write_new_db

def main():
	source_db_paths, field_names = read_browser_db.firefox()
	
	prepped_records = read_browser_db.read_browser_database(filepaths=source_db_paths, fieldnames=field_names)
	# gives a generator that yields all the records across all profiles.
	yield_source_records = (record for profile_ in prepped_records for record in profile_)
	
	sink_db_path = helpers.filepath_from_another('merged_fx_db.sqlite')
	url_hash_log_file = helpers.filepath_from_another('url_hash_log.bin')
	
	# target database connection object
	sink_db_info = db_handler.connect_db(db_file=sink_db_path)
	
	processed_url_hashes = write_new_db.merge_databases(source_record_yielder=yield_source_records, sink_db_info=sink_db_info, print_records=4000)
	
	filemodes = {True: 'ab', False: 'wb'}
	filemode_ = filemodes[os.path.exists(url_hash_log_file)]
	with open(url_hash_log_file, filemode_) as write_obj:
		write_obj.write(processed_url_hashes)


main()
