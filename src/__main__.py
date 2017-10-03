import os

import db_handler
import deduplicator
import helpers
import read_browser_db
import write_new_db


source_db_paths = read_browser_db.firefox()
prepped_records = read_browser_db.read_browser_database(filepaths=source_db_paths)  # gives a generator that yields all the records across all profiles.
yield_source_records = (record for profile_ in prepped_records for record in profile_)

sink_db_path = helpers.filepath_from_another('newtest_not_atomized.sqlite')
url_hash_log_file = helpers.filepath_from_another('url_hash_log.bin')

sink_db_info = db_handler.connect_db(db_file=sink_db_path)

url_hashes = write_new_db.merge_databases(source_record_yielder=yield_source_records, sink_db_info=sink_db_info, print_records=4000)
filemodes = {True: 'ab', False: 'wb'}
filemode_ = filemodes[os.path.exists(url_hash_log_file)]
with open(url_hash_log_file, filemode_) as write_obj:
	write_obj.write(url_hashes)
	
	# write_url_hash_to_log(url_hash_log_file, new_record=record)
	

	# url_hash_log = read_url_hash_from_log(url_hash_log_file)
	# url_hash_ids = url_hash_log
	
	# redundant = bool(url_hash_ids.get(curr_url_hash, None))
	
	# deduplicator.deduplicate_records(new_record=record, sink_db_path=sink_db_path)
# write_new_db.write_to_json(sink_db_path, record_yielder=yield_source_records)
# for record in yield_source_records:
# 	unique_record = deduplicator.deduplicate_records(record)
# 	print(unique_record)
'CREATE TABLE moz_places (id, url, title, rev_host, visit_count, hidden, typed, favicon_id, frecency, last_visit_date, guid, foreign_count, url_hash, description, preview_image_url)'
