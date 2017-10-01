#:TODO: Algorithm.
'''
{prologue: File with url_hash: id}
0. Open Source DB from Profile. - Done in read_browser_db()
1. Open Sink DB. - Done in write_new_db()
2. Fetch source record from Profile. - Done in read_browser_db()
3. Open URL Archive.
4. Get url_hash
5. check if URL hash in archive.
 - If Yes, Update Last Visited & Visit counts using primary key id, or url_hash.
 - If No, Change id to next available value, write the record to sink. Add {url_hash: id} to archive.
6. Commit.
7. Open next profile.
8. Repeat.
Close Source & Sink DBs.

'''
import jsonlines
import os

import write_new_db


filepath_from_another = lambda filepath, filename: os.path.join(os.path.dirname(filepath), filename)

def manage_url_hash_log(record=None):
	'''
	Open the archive, load url_hashes (keys) from it as a set.
	:return: set of url hashes
	'''
	# Open url_hash archive.
	if record:
		curr_url_hash = list(record.keys())[0]
		record_id = record[curr_url_hash ]['id']
		write_hash = ''.join([str(curr_url_hash), ': ', str(record_id), ', '])
		try:
			with open ('url_hash_log.txt', 'a') as hash_log_obj:
				hash_log_obj.write(write_hash)
		except FileNotFoundError:
			with open ('url_hash_log.txt', 'w') as hash_log_obj:
				hash_log_obj.write(write_hash)
	else:
		try:
			with open('url_hash_log.txt', 'r') as hash_log_obj:
				url_hashes = hash_log_obj.read()
			url_hashes = [int(url_hash) for url_hash in url_hashes.split(', ') if url_hash.isnumeric()]
		except FileNotFoundError:
			url_hashes = []
		finally:
			return url_hashes
	

def redundant_url_hash(record, url_hashes):
	'''
	Reads the url_hash & id field from record, membership test with archive set.
	Returns {url_hash: id} or None
	:param record:
	'''
	curr_url_hash = list(record.keys())[0]
	return curr_url_hash, curr_url_hash in url_hashes
	

def update_record(record, url_hash, json_db):
	'''
	Finds existing record in Sink DB using hash_val or id.
	Updates last visited to latest, adds the visit counts.
	:param record:
	:type record:
	:return:
	:rtype:
	'''
	update_fields = ['last_visit_date', 'visit_count']
	with jsonlines.open('json_db', 'r') as json_read_obj:
		edit_record = [json_db_record for json_db_record in json_read_obj if json_db_record == url_hash]
		print(edit_record)
		for field in update_fields:
			print('new rocrd', record[url_hash][field])
	input('ENTER to continue.')
	print('update record not implemented.')


def insert_record(record):
	'''
	Changes record id to next available.
	:param record: record
	:type record:
	:return:
	:rtype:
	'''
	pass

	
# save/commit changes.
def deduplicate_records(database_records, json_path, new_record):
	# global write_to_database
	url_hashes = manage_url_hash_log()
	curr_url_hash, redundant = redundant_url_hash(new_record, url_hashes)
	if redundant:
		update_record(new_record, database_records)
	else:
		manage_url_hash_log(record=new_record)
		write_new_db.write_to_json(json_path, record_yielder=database_records)
		
		return new_record
		# write_new_db.write_to_db(database=write_to_database, new_record=new_record, table='moz_places')


# write_to_database = filepath_from_another(__file__, 'test.sqlite')
if __name__ == '__main__':
	from show import quick_read_record
	# test_deduplicate_records()
	print('*' * 50)
	
	print(os.getcwd())
	# quick_read_record(database=write_to_database)
