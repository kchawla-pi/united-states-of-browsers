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
import write_new_db
from read_browser_db import quick_read_record


def manage_url_hash_log(url_hash=None):
	'''
	Open the archive, load url_hashes (keys) from it as a set.
	:return: set of url hashes
	'''
	# Open url_hash archive.
	if url_hash:
		write_hash = ''.join([str(url_hash), ', '])
		url_hashes = []
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
	


def update_record(record):
	'''
	Finds existing record in Sink DB using hash_val or id.
	Updates last visited to latest, adds the visit counts.
	:param record:
	:type record:
	:return:
	:rtype:
	'''
	pass


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
def deduplicate_records(record):
	global write_to_database
	url_hashes = manage_url_hash_log()
	curr_url_hash, redundant = redundant_url_hash(record, url_hashes)
	if redundant:
		update_record(record)
	else:
		manage_url_hash_log(url_hash=curr_url_hash)
		write_new_db.write_to_db(database=write_to_database, record=record, table='moz_places')


def test_deduplicate_records():
	test_records = [
		{47356370932282:
			 {'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
			  'rev_host': 'gro.allizom.www.', 'visit_count': 10, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': 1503579273203000,
			  'guid': 'NNqZA_f2KHI1',
			  'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
			  'preview_image_url': None}
		 },
		{47357795150914:
			 {'id': 2, 'url': 'https://support.mozilla.org/en-US/products/firefox', 'title': None,
			  'rev_host': 'gro.allizom.troppus.', 'visit_count': 20, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': 268505095842199,
			  'guid': '4xhwpotXndUs',
			  'foreign_count': 1, 'url_hash': 47357795150914, 'description': None,
			  'preview_image_url': None}
		 },
		{47357795150914:
			{'id': 2, 'url': 'https://support.mozilla.org/en-US/products/firefox',
			'title': None,
			'rev_host': 'gro.allizom.troppus.', 'visit_count': 2, 'hidden': 0,
			'typed': 0,
			'favicon_id': None, 'frecency': 76, 'last_visit_date': 1498227024629000,
			'guid': '4xhwpotXndUs',
			'foreign_count': 1, 'url_hash': 47357795150914, 'description': None,
			'preview_image_url': None}
		 },
		]

	expected_database = [
		{47356370932282:
			 {'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
			  'rev_host': 'gro.allizom.www.', 'visit_count': 10, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': 268505095842199,
			  'guid': 'NNqZA_f2KHI1',
			  'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
			  'preview_image_url': None}
		 },
		{47357795150914:
			 {'id': 2, 'url': 'https://support.mozilla.org/en-US/products/firefox', 'title': None,
			  'rev_host': 'gro.allizom.troppus.', 'visit_count': 22, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': None, 'guid': '4xhwpotXndUs',
			  'foreign_count': 1, 'url_hash': 47357795150914, 'description': None,
			  'preview_image_url': None}
		 },
		]
	returned_output = []
	for test_case in test_records:
		returned_output.append(deduplicate_records(test_case))
	print(returned_output)
	print('last_visit_date not fixed in one of the records. Test result invalid until it is.',
	      returned_output == expected_database)


write_to_database = 'test3.sqlite'
if __name__ == '__main__':
	test_deduplicate_records()
	quick_read_record(database=write_to_database)
