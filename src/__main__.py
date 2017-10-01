import jsonlines
import os
import read_browser_db

import deduplicator
import write_new_db


file_paths = read_browser_db.firefox()
prepped_records = read_browser_db.read_browser_db(filepaths=file_paths)  # gives a generator that yields all the records across all profiles.

json_path = os.path.join(os.path.dirname(__file__), 'test.json')
yield_records = (record for profile_ in prepped_records for record in profile_)
deduplicator.deduplicate_records(database_records=yield_records, json_path=json_path, new_record=None)
# write_new_db.write_to_json(json_path, record_yielder=yield_records)
# for record in yield_records:
# 	unique_record = deduplicator.deduplicate_records(record)
# 	print(unique_record)
